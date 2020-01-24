from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser, Group
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
import datetime
from django.db.models.fields import DateTimeField

from django.db.models.signals import post_save, pre_save

"""
Constants
"""
USER_TIME = 52 # 52 weeks once user created user is active

DEFAULT_GROUP_LEAVE_TIME = 4 # after 4 weeks from registration user will be out / inactive from group

def end_date_time():
	return datetime.datetime.now() - datetime.timedelta(DEFAULT_GROUP_LEAVE_TIME)


"""
Custom Field Declaration 
"""
class UTCField(DateTimeField):

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = datetime.datetime.now()
            setattr(model_instance, self.attname, value)
            return value
        else:
            value = getattr(model_instance, self.attname)
            if not isinstance(value, datetime):
                value = datetime.datetime.fromtimestamp(int(value))
                setattr(model_instance, self.attname, value)
            return super(UTCField, self).pre_save(model_instance, add)




# Create your models here.
class UserManager(BaseUserManager):
	def _create_user(self, first_name, last_name, email, contact_no, password, is_superuser, is_staff, **extra_fields):
		if not email:
			raise ValueError('Users must have an email address')
		now = timezone.now()
		first_name = first_name.capitalize()
		last_name = last_name.capitalize()
		contact_no = contact_no.strip()
		email = self.normalize_email(email)
		user = self.model(
			first_name = first_name,
			last_name = last_name,
			email=email,
			contact_no = contact_no,
			is_staff=is_staff, 
			is_active=True,
			is_superuser=is_superuser, 
			last_login=now,
			date_joined=now, 
			**extra_fields
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, first_name, last_name, email, contact_no, password, **extra_fields):
		return self._create_user(first_name, last_name, email, contact_no, password, False, False, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		user=self._create_user("", "", email, "", password, True, True, **extra_fields)
		user.save(using=self._db)
		return user


class AlgonautsUser(AbstractBaseUser, PermissionsMixin):
	first_name = models.CharField(max_length=64)
	last_name = models.CharField(max_length=64)
	email = models.EmailField(max_length=254, unique=True)
	contact_no = models.CharField(max_length=10) #RegexValidator(regex = r'^[0-9]*$')
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	last_login = models.DateTimeField(null=True, blank=True)
	date_joined = models.DateTimeField(auto_now_add=True)
	# algo_credits = models.IntegerField()

	USERNAME_FIELD = 'email'
	EMAIL_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()

	def get_absolute_url(self):
		return "/users/%i/" % (self.pk)
	def __str__(self):
		return "_".join((str(self.email)).split("@"))

class UserGroupType(models.Model):
	type_name = models.CharField(max_length=128)
	max_members = models.IntegerField()
	min_members = models.IntegerField()
	standard_group = models.CharField(max_length=128)
	def __str__(self):
		return str(self.type_name)

class UserGroup(models.Model):
	user_group_type_id = models.ForeignKey(UserGroupType, on_delete = models.CASCADE)
	members = models.ManyToManyField(
		AlgonautsUser,
		through='UserGroupMapping',
		through_fields=('user_group_id', 'user_profile_id'),
	)
	registration_time = models.DateTimeField(auto_now=True)
	def __str__(self):
		return "%".join([str(self.id), str(self.user_group_type_id),] )


class ReferralOffer(models.Model):
    offer_name = models.CharField(max_length=100) 
    def __str__(self):
    	return str(self.offer_name)


class Referral(models.Model):
	referral_code = models.IntegerField()
	referred_by = models.ForeignKey(AlgonautsUser, on_delete=models.CASCADE, related_name='by') 
	referred_to = models.ForeignKey(AlgonautsUser, on_delete=models.CASCADE, related_name='to') 
	referral_time = models.DateTimeField()
	referral_offer_id = models.ForeignKey(ReferralOffer, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.referral_code)


class UserGroupMapping(models.Model):
	user_group_id = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
	user_profile_id = models.ForeignKey(AlgonautsUser, on_delete= models.CASCADE)
	time_added = models.DateTimeField(auto_now=True)
	time_removed = models.DateTimeField(default = end_date_time, null=True, blank=True)
	group_admin = models.BooleanField(default=False)

	@property
	def is_present(self):
		if datetime.datetime.now > self.time_removed : 
			return True
		return False

	def __str__(self):
		return "#".join([str(self.user_profile_id) , str(self.user_group_id)])
  
# Code to add permission to group 
def create_individual_user_group(sender, instance, **kwargs):
	indiv = UserGroupType.objects.get(type_name='Individual')

	group = UserGroup.objects.create(user_group_type_id=indiv)
	# group.save()  

	group_map = UserGroupMapping.objects.create(user_group_id = group, user_profile_id = instance, time_added = datetime.datetime.now(), \
					time_removed = datetime.datetime.now() + datetime.timedelta(weeks=4), group_admin = True)
	# group_map.save()
	return



def validate_group_restriction(sender, instance, **kwargs):
	mems = UserGroupMapping.objects.filter(user_group_id = instance.user_group_id)
	unq = UserGroupMapping.objects.filter(user_group_id = instance.user_group_id, user_profile_id = instance.user_profile_id).count()
	if unq > 1:
		instance.delete()
		return
	
	mzx = UserGroupType.objects.filter(type_name = instance.user_group_id.user_group_type_id)[0]
	if mzx.max_members < len(mems):
		instance.delete()
		return
	
	


# DB Signals 
post_save.connect(create_individual_user_group, sender=AlgonautsUser, dispatch_uid="users.models.AlgonautsUser")

post_save.connect(validate_group_restriction, sender= UserGroupMapping, dispatch_uid="users.models.UserGroupMapping")


