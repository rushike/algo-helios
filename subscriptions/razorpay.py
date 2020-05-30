import logging
import datetime
import num2words

from helios.settings import client, RAZORPAY_KEY, TAXES, GSTIN_NO, PAN_ID
import users.functions
import subscriptions.functions
import products.functions

from razorpay.resources.base import Resource
from razorpay.resources.invoice import Invoice
from razorpay.constants.url import URL


logger = logging.getLogger('normal')

class Items(Resource):
    def __init__(self, client=None):
        super(Items, self).__init__(client)
        self.base_url = '/items' # ''.join([URL.BASE_URL, '/items'])

    def create(self, data={}, **kwargs):
        """"
        Create items from given dict
        Args:
            data : Dictionary having keys using which Plan has to be created
        Returns:
            Plan Dict which was created
        """
        url = self.base_url
        return self.post_url(url, data, **kwargs)

    def fetch(self, plan_id, data={}, **kwargs):
        """"
        Fetch items for given Id
        Args:
            plan_id : Id for which Plan object has to be retrieved
        Returns:
            Plan dict for given subscription Id
        """
        return super(Items, self).fetch(plan_id, data, **kwargs)

    def all(self, data={}, **kwargs):
        """"
        Fetch all items entities
        Returns:
            Dictionary of plan data
        """
        return super(Items, self).all(data, **kwargs)

    def edit(self, item_id, data={}, **kwargs):
        """"
        Update an item
        
        Args:
            invoice_id : Id for delete the invoice
            data : Dictionary having keys using which invoice have to be updated
        Returns:
            Its response is the invoice entity, similar to create/update API response. Its status now would be issued.
            Refer https://razorpay.com/docs/invoices/api/#entity-structure
        """
        url = "{}/{}".format(self.base_url, item_id)
        return self.patch_url(url, data, **kwargs)

class AlgonautsInvoice(Invoice):
    def paid(self, invoice_id, **kwargs):
        """"
        Issues an invoice in draft state
        Args:
            invoice_id : Id for delete the invoice
        Returns:
            Its response is the invoice entity, similar to create/update API response. Its status now would be issued.
        """
        url = "{}/{}/paid".format(self.base_url, invoice_id)
        return self.post_url(url, {}, **kwargs)

setattr(client, 'items', Items(client))
setattr(client, 'invoice', AlgonautsInvoice(client))

def create_razorpay_customer(user):
    user = users.functions.get_user_object(user)
    return client.customer.create(
        data={
            "name": ' '.join([user.first_name, user.last_name]),
            "email": user.email,
            "contact": user.contact_no,
            "fail_existing": "0",
        }
    )

def create_razorpay_invoice(user, plan, subscription_type):
    """Since razorpay don't support GST invoice through API, We have TAXES vairable in Django settings
    and considering 
        amount   : total amount (including taxes)
        tax_rate : total tax applicable (including cgst, sgct, igst) 
    """
    try :
        user = users.functions.get_user_object(user)
        plan = subscriptions.functions.get_plan_object(plan)
        period = subscriptions.functions.get_subscription_type_object(subscription_type)
        customer = create_razorpay_customer(user)
        invoice =  client.invoice.create(
            data = {
                "type": "invoice",
                "description": "Invoice for " + "-".join([plan.user_group_type_id.type_name, plan.plan_name, "monthly"]),
                "customer": {
                    "name": customer["name"],
                    "contact": customer["contact"],
                    "email": customer["email"]
                },
                "line_items": [
                    {
                        "name": "-".join([plan.user_group_type_id.type_name, plan.plan_name.replace("#", "-"), "monthly"]),
                        "amount": int(plan.price_per_year * (100 + TAXES["total"])),
                        "currency": "INR",
                        "description": "Item : " + "-".join([plan.user_group_type_id.type_name, plan.plan_name.replace("#", "-"), "monthly"]) + " billed from : {} - {}",
                        "tax_rate" : TAXES["total"],
                    }
                ],
                "sms_notify": 0,
                "email_notify": 0,
            }
        )
        return invoice
    except Exception as e:
        logger.error(f"Error : {e} occurred while creating the invoice")

def create_razorpay_item(name, description, amount, currency = "INR"):
    return client.items.create(
        data = {
            "name" : name,
            "description" : description,
            "amount" :  amount,
            "currency" :  currency
        }
    )

def get_line_item(plan, period = 'monthly'):
    if period.lower() == 'monthly':
        plan_id = plan.razorpay_plan_per_month_id
        razor_plan = client.plan.fetch(plan.razorpay_plan_per_month_id)
    elif period.lower() == 'yearly':
        plan_id = plan.razorpay_plan_per_year_id
        razor_plan = client.plan.fetch(plan.razorpay_plan_per_year_id)
    return razor_plan['item']

def create_or_update_razorpay_plan(force = False):
    all_plans = subscriptions.functions.get_all_active_plans()
    plans = client.plan.all()
    for plan in all_plans:
        if force or plan.razorpay_plan_per_month_id == None:
            razor_plan = client.plan.create(data = {
                "period": "monthly",
                "interval": 1,
                "item": {
                    "name": "-".join([plan.user_group_type_id.type_name, plan.plan_name, "monthly"]),
                    "amount": plan.price_per_month,
                    "currency": "INR",
                    "description": " ",
                    "tax_rate" : 18
                },
            })
            plan.razorpay_plan_per_month_id = razor_plan['id']
            plan.save(update_fields=['razorpay_plan_per_month_id'])
        if force or plan.razorpay_plan_per_year_id == None:
            razor_plan = client.plan.create(data = {
                "period": "yearly",
                "interval": 1,
                "item": {
                    "name"         : "-".join([plan.user_group_type_id.type_name, plan.plan_name, "monthly"]),
                    "total_amount" : plan.price_per_year,
                    "currency"     : "INR",
                    "description"  : "",
                },
            })
            plan.razorpay_plan_per_year_id = razor_plan['id']
            plan.save(update_fields=['razorpay_plan_per_year_id'])


def create_invoice_context(invoice_id):
    """Here while making invoice we need start and end date of particular subscriptions item
    There need to be plan map, or we can use direct items api, to create particular map
    """
    try:
        context = client.invoice.fetch(invoice_id)
        subscription = subscriptions.functions.get_subscriptions_from_invoice_id(invoice_id)
        startdate = subscription.subscription_start.date()
        enddate = subscription.subscription_end.date()
        logger.debug(f"invoice fetch from razorpay : {context}")
        # for item tax preparation
        total_cgst = 0
        total_sgst = 0
        total_igst = 0
        total_taxable_amount = 0
        total_amount = 0
        for item in context["line_items"]:
            item["amount"] /= 100
            tax_amt  = round(item["amount"] / (100 + TAXES["total"]) * 100, 2)
            cgst_amt = 0 if TAXES["cgst"] == 0 else round(item["amount"] * TAXES["cgst"] / 100, 2)
            sgst_amt = 0 if TAXES["sgst"] == 0 else round(item["amount"] * TAXES["sgst"] / 100, 2)
            igst_amt = 0 if TAXES["igst"] == 0 else round(item["amount"] * TAXES["igst"] / 100, 2)
            item.update({
                "taxable_amount" : tax_amt,
                "tax_rate"     : TAXES["total"],
                "cgst"         : TAXES["cgst"],
                "cgst_tax"     : cgst_amt,
                "sgst"         : TAXES["sgst"],
                "sgst_tax"     : sgst_amt,
                "igst"         : TAXES["igst"],
                "igst_tax"     : igst_amt,
                "description"  : item["description"].format(startdate, enddate)
            })

            total_amount         += item["amount"]
            total_taxable_amount += tax_amt
            total_cgst           += cgst_amt
            total_sgst           += sgst_amt
            total_igst           += igst_amt

        # outer details
        context.update({
            "gstin_no"        : GSTIN_NO,
            "pan_id"          : PAN_ID,
            "time_of_supply"  : datetime.datetime.fromtimestamp(context["paid_at"]).date(),
            "place_of_supply" : "Mumbai",
            "invoice_number"  : context["id"],
            "state"           : "Maharastra",
            "state_code"      : 27,
            "cust_name"       : context["customer_details"]["name"],
            "cust_address"    : "",
            "cust_gstin_no"   : "NOT APPLIED",
            "cust_state"      : "Maharashtra",
            "cust_state_code" : 27,

            "total_amount"    : total_amount,
            "total_taxable_amount" : total_taxable_amount,
            "total_cgst"      :total_cgst,
            "total_sgst"      :total_sgst,
            "total_igst"      :total_igst,
            "total_amount_in_words" : num2words.num2words(total_amount, lang = "en_IN")
        })
            
        return context
    except Exception as e:
        logger.error(f"Error : {e} occurred, no invoice created of razorpay with invoice_id : {invoice_id}")