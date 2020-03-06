from products.models import UserProductFilter, Product
from channels.db import database_sync_to_async
import users.functions
import json


def get_user_filter_for_product(user, product):
    return UserProductFilter.objects.filter(user_id = user, product_id = product).first()

@database_sync_to_async
def get_user_filter_for_product_async(user, product):
    user_product_filter = get_user_filter_for_product(user, product)
    return json.load(user_product_filter.filter_attributes)

def get_product_names_from_groups(groups):
    groups = list(map(lambda group : group.replace("-", "#"), groups))

@database_sync_to_async
def get_user_subs_groups_async(user):
    products = users.functions.get_user_subs_product(user)
    return list(map(lambda product: product.product_name.replace("#", "-").lower(), products))

def get_user_subs_groups(user):
    products = users.functions.get_user_subs_product(user)
    return list(map(lambda product: product.product_name.replace("#", "-").lower(), products))
