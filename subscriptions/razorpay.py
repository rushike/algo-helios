from helios.settings import client, RAZORPAY_KEY
import users.functions
import subscriptions.functions
import products.functions

from razorpay.resources.base import Resource
from razorpay.resources.invoice import Invoice
from razorpay.constants.url import URL

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
        print("url : ", url)
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
                    "name": "-".join([plan.user_group_type_id.type_name, plan.plan_name, "monthly"]),
                    "amount": int(plan.price_per_year * 100),
                    "currency": "INR",
                    "description": ""
                }
            ],
            "sms_notify": 1,
            "email_notify": 1,
        }
    )
    return invoice

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
    for plan in all_plans:
        print(f"name : {plan.plan_name}, month : {plan.price_per_month}, year : {plan.price_per_year}")
        if force or plan.razorpay_plan_per_month_id == None:
            razor_plan = client.plan.create(data = {
                "period": "monthly",
                "interval": 1,
                "item": {
                    "name": "-".join([plan.user_group_type_id.type_name, plan.plan_name, "monthly"]),
                    "amount": plan.price_per_month,
                    "currency": "INR",
                    "description": " "
                },
            })
            plan.razorpay_plan_per_month_id = razor_plan['id']
            plan.save(update_fields=['razorpay_plan_per_month_id'])
        if force or plan.razorpay_plan_per_year_id == None:
            razor_plan = client.plan.create(data = {
                "period": "yearly",
                "interval": 1,
                "item": {
                    "name": "-".join([plan.user_group_type_id.type_name, plan.plan_name, "monthly"]),
                    "amount": plan.price_per_year,
                    "currency": "INR",
                    "description": ""
                },
            })
            plan.razorpay_plan_per_year_id = razor_plan['id']
            plan.save(update_fields=['razorpay_plan_per_year_id'])

