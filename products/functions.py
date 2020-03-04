from products.models import UserProductFilter, Product
import users.functions


import json


def get_product_object(product):
    if type(product) == str: return Product.objects.filter(product_name__iexact = product).first()
    if type(product) == int: return Product.objects.filter(id = product).first()
    if type(product) == Product: return product
    return None


def add_user_products_filter(user_id, product_id, filter_attributes):
    user_id = users.functions.get_user_object(user_id)
    product_id = get_product_object(product_id)
    if type(filter_attributes) == dict:
        filter_attributes = json.dumps(filter_attributes, indent = 4)
    filter_obj = UserProductFilter.objects.update_filter(user_id, product_id, filter_attributes)