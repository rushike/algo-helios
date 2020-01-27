
from django.db.models.signals import post_save, pre_save
import datetime


from users.models import AlgonautsUser, UserGroup, UserGroupMapping, UserGroupType


# Code to add permission to group 
def create_individual_user_group(sender, instance, **kwargs):
	indiv = UserGroupType.objects.get(type_name='individual')

	group = UserGroup.objects.create_user_group(user_group_type_id=indiv, registration_time = datetime.datetime.now(), admin = instance)
	# group.save()

	group_map = UserGroupMapping.objects.create(user_group_id = group, user_profile_id = instance, time_added = datetime.datetime.now(), \
					time_removed = datetime.datetime.now() + datetime.timedelta(weeks=4), group_admin = True)
	# group_map.save()
	return



# def validate_group_restriction(sender, instance, **kwargs):
# 	mems = UserGroupMapping.objects.filter(user_group_id = instance.user_group_id)
# 	unq = UserGroupMapping.objects.filter(user_group_id = instance.user_group_id, user_profile_id = instance.user_profile_id).count()
# 	if unq > 1:
# 		instance.delete()
# 		return
	
# 	mzx = UserGroupType.objects.filter(type_name = instance.user_group_id.user_group_type_id)[0]
# 	if mzx.max_members < len(mems):
# 		instance.delete()
# 		return
	
	


# DB Signals 
post_save.connect(create_individual_user_group, sender=AlgonautsUser, dispatch_uid="users.models.AlgonautsUser")

# post_save.connect(validate_group_restriction, sender= UserGroupMapping, dispatch_uid="users.models.UserGroupMapping")


