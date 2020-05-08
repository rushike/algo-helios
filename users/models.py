from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser, Group
# from django.contrib.localflavor._in.models import INStateField, INZipCodeField
from localflavor.in_.models import  INStateField
from django.db import models
from django.core.validators import RegexValidator,MinLengthValidator
from django.utils import timezone
from django.db.models.fields import DateTimeField
from django.db.models.signals import post_save, pre_save
import datetime, random, string, time, os, base64, pytz
from hashlib import md5
import pytz, datetime


"""
Constants or Functions
Calculates the default end date for user to removed
"""
REFERRAL_CODE_LEN = 8

def end_date():
		return datetime.timedelta(weeks=52 * 10) + datetime.datetime.now(pytz.timezone('UTC'))

def get_unique_referral_code():
	token=os.urandom(REFERRAL_CODE_LEN)
	return base64.urlsafe_b64encode(token).decode('utf8')[:REFERRAL_CODE_LEN]


class UserManager(BaseUserManager):
	
	def _create_user(self, first_name, last_name, email, contact_no, password, is_superuser, is_staff, **extra_fields):
		now = datetime.datetime.now(pytz.timezone('UTC'))
		first_name = first_name.capitalize()
		last_name = last_name.capitalize()
		contact_no = contact_no.strip()
		email = self.normalize_email(email)
		referral_code = get_unique_referral_code()
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
			referral_code = referral_code,
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
	algo_credits = models.IntegerField(default=0)
	referral_code = models.CharField(max_length=REFERRAL_CODE_LEN, validators=[MinLengthValidator(4)], default=get_unique_referral_code)

	USERNAME_FIELD = 'email'
	EMAIL_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()

	class Meta:
		unique_together = ('referral_code',)

	def get_absolute_url(self):
		return "/users/%i/" % (self.pk)

	def join_to_group(self, group_id): # method add user(self) to the specific group with group_id 
		user_group_id = UserGroup.objects.get(id = group_id)
		mapper = UserGroupMapping.objects.create_user_group_mapping(user_profile_id= self, user_group_id=user_group_id, group_admin= False)
		return mapper

	def __str__(self):
		return "_".join((str(self.email)).split("@"))


class Address(models.Model):
	email = models.ForeignKey(AlgonautsUser, on_delete = models.CASCADE,related_name="a_email")
	line1 = models.CharField(max_length = 64)
	line2 = models.CharField(max_length = 64)
	city = models.CharField(max_length = 32)
	state = INStateField()
	zipcode = models.CharField(max_length = 12)

class UserGroupTypeManager(models.Manager):
	def create_user_group_type(self):
		return



class UserGroupType(models.Model):
	type_name = models.CharField(max_length=128)
	max_members = models.IntegerField(default=1)
	min_members = models.IntegerField(default=1)
	standard_group = models.BooleanField(default=True, blank=True)
	eligible_for_trial = models.BooleanField(default=True)
	objects = UserGroupTypeManager()

	class Meta:
		unique_together = ('type_name', 'max_members', 'min_members')

	def __str__(self):
		return str(self.type_name)


class UserGroupManager(models.Manager):
	def create_user_group(self, user_group_type_id, admin, multiplier = 1):
		#can validate if any restrictions, returns None if, user_group with user_group_type, admin already present
		user_group = UserGroup.objects.filter(user_group_type_id = user_group_type_id, admin = admin, multiplier = multiplier)
		if user_group.exists():
			return user_group.first()
		user_group = self.model(user_group_type_id = user_group_type_id, registration_time = datetime.datetime.now, admin = admin)
		user_group.save(using=self._db)
		return user_group


class UserGroup(models.Model):
	user_group_type_id = models.ForeignKey(UserGroupType, on_delete = models.CASCADE,related_name="ug_user_group_type_id")
	memb = models.ManyToManyField(
		AlgonautsUser,
		through='UserGroupMapping',
		through_fields=('user_group_id', 'user_profile_id'),
	) 
	registration_time = models.DateTimeField(auto_now=True)
	admin = models.ForeignKey(AlgonautsUser, on_delete= models.CASCADE, related_name="ug_admin")
	multiplier = models.IntegerField(default=1) # describle quatity of subscription simutanouesly allowed in on subscription
	objects = UserGroupManager()

	class Meta:
		unique_together = ('user_group_type_id','admin')
		 
	def __str__(self):
		return "%".join([str(self.id), str(self.user_group_type_id),] )


class ReferralOfferManager(models.Manager):
	def create_referral_offer(self, offer_name, offer_credits_to, offer_credits_by, offer_start, offer_end, offer_active):
		if offer_active:
			ReferralOffer.objects.filter(offer_active = True).update(offer_active = False)
		referral_offer = self.model(offer_name = offer_name,
									 offer_credits_to = offer_credits_to, 
									 offer_credits_by = offer_credits_by, 
									 offer_start = datetime.datetime.now, 
									 offer_end = offer_end, 
									 offer_active = offer_active)
		referral_offer.save(using=self._db)


class ReferralOffer(models.Model):
	offer_name = models.CharField(max_length=100) 
	offer_credits_to = models.IntegerField()
	offer_credits_by = models.IntegerField()
	offer_start = models.DateTimeField(auto_now=True)
	offer_end = models.DateTimeField(blank = True)
	offer_active = models.BooleanField(default=True)
	objects = ReferralOfferManager()
	
	def __str__(self):
		return str(self.offer_name)	


class Referral(models.Model):
	referral_code = models.CharField(max_length=REFERRAL_CODE_LEN)
	referred_by = models.ForeignKey(AlgonautsUser, on_delete=models.CASCADE, related_name='r_referred_by') 
	referred_to = models.ForeignKey(AlgonautsUser, on_delete=models.CASCADE, related_name='r_reffered_to') 
	referral_time = models.DateTimeField()
	referral_offer_id = models.ForeignKey(ReferralOffer, on_delete=models.CASCADE, related_name="r_referral_offer_id")
	credits_granted = models.BooleanField(default = False)
	class Meta:
		unique_together = ('referred_to',)

	def __str__(self):
		return str(self.referral_code)


class UserGroupMappingManager(models.Manager):

	def create_user_group_mapping(self, user_profile_id, user_group_id, group_admin): # delta period in number of weeks
		if user_group_id is None: return # if group is not form due to some err, don't add user_group_mapping 
		mems = UserGroupMapping.objects.filter(
											user_group_id = user_group_id, 
											time_removed__gt = datetime.datetime.now(pytz.timezone('UTC'))
											).count() # neccessary to check how many members currently present in group
		unq = UserGroupMapping.objects.filter(
											user_group_id = user_group_id, 
											user_profile_id = user_profile_id, 
											time_removed__gt = datetime.datetime.now(pytz.timezone('UTC'))
											).exists() # to check if duplicate entry 
		if unq: return # allow one user to be admin of only one user group of particular type
		mzx = UserGroupType.objects.filter(type_name = user_group_id.user_group_type_id)[0].max_members # checks the maximum number allowed by particular group
		if mzx < mems: return # do not add more than max number specified
		mapper = self.create(
				user_group_id = user_group_id, 
				user_profile_id = user_profile_id, 
				time_added = datetime.datetime.now(pytz.timezone('UTC')),
				time_removed = datetime.timedelta(weeks=52 * 10) + datetime.datetime.now(pytz.timezone('UTC')),
				group_admin = True)
		mapper.save(using = self._db)
		return mapper
	
	def delete_user_from_all_groups(self, user_profile_id, group_admin):
		if not user_profile_id and not group_admin: return # if group is not form due to some err, don't add user_group_mapping 
		user_profile_id = user_profile_id if isinstance(user_profile_id, AlgonautsUser) else AlgonautsUser.objects.filter(email = user_profile_id).first()
		group_map = UserGroupMapping.objects.filter(user_profile_id = user_profile_id)
		user_groups_id = group_map.values("user_group_id")
		admin = AlgonautsUser.objects.filter(email = group_admin) if not isinstance(group_admin, AlgonautsUser) else group_admin
		user_group = UserGroup.objects.filter(id__in = user_groups_id, admin__in = admin)
		if user_group.exists():
			group_map = group_map.filter(user_group_id__in = user_group)
			group_map.update(time_removed = datetime.datetime.now(pytz.timezone('UTC')))

	def delete_user_from_group(self, user_profile_id, group_id, group_admin):
		if not user_profile_id or not group_admin or not group_id: return # if group is not form due to some err, don't add user_group_mapping 
		user_profile_id = user_profile_id \
							if isinstance(user_profile_id, AlgonautsUser) \
							else AlgonautsUser.objects.filter(email = user_profile_id).first()
		group_map = UserGroupMapping.objects.filter(user_profile_id = user_profile_id, user_group_id = group_id)
		admin = AlgonautsUser.objects.filter(email = group_admin).first() \
						if not isinstance(group_admin, AlgonautsUser) \
						else group_admin

		if admin.email == group_id.admin.email:
			group_map = group_map.filter(time_removed__gt = datetime.datetime.now(pytz.timezone('UTC')))
			group_map.update(time_removed = datetime.datetime.now(pytz.timezone('UTC')))


class UserGroupMapping(models.Model):
	user_group_id = models.ForeignKey(UserGroup, on_delete=models.CASCADE, related_name="ugm_user_group_id")
	user_profile_id = models.ForeignKey(AlgonautsUser, on_delete= models.CASCADE, related_name="ugm_user_profile_id")
	time_added = models.DateTimeField(auto_now=True)
	time_removed = models.DateTimeField(default = end_date)
	group_admin = models.BooleanField(default=False)
	objects = UserGroupMappingManager()

	@property
	def is_present(self):
		return datetime.datetime.now > self.time_removed  
			
	@property
	def get_user_group_type(self):
		return self.user_group_id.user_group_type_id

	def __str__(self):
		return "#".join([str(self.user_profile_id) , str(self.user_group_id)])


class UserFeedback(models.Model):
	email = models.ForeignKey(AlgonautsUser, on_delete=models.CASCADE)
	feedback_message = models.CharField(max_length=1024)
	category_name = models.CharField(max_length=20)
	subject = models.CharField(max_length= 128)

	def __str__(self):
		return self.category_name

  
# Code to add permission to group 
def create_individual_user_group(sender, instance, **kwargs):
	indiv = UserGroupType.objects.get_or_create(type_name='individual')[0]
	group = UserGroup.objects.create_user_group(user_group_type_id=indiv, admin = instance)
	if group is None : return
	group_map = UserGroupMapping.objects.create_user_group_mapping(user_group_id = group, user_profile_id = instance, group_admin = True)

def create_usergroup_mapping(sender, instance, **kwargs):
	group_map = UserGroupMapping.objects.create_user_group_mapping(user_group_id = instance, user_profile_id = instance.admin, group_admin = True)

def active_referral_offer_checks(sender, instance, **kwargs):
	# ReferralOffer.
	offer_active = instance.offer_active
	if offer_active:
		ReferralOffer.objects.filter(offer_active = True).update(offer_active = False)
			
# DB Signals 
post_save.connect(create_individual_user_group, sender=AlgonautsUser, dispatch_uid="users.models.AlgonautsUser") # to create users individual group after user creation

post_save.connect(create_usergroup_mapping, sender=UserGroup, dispatch_uid="users.models.UserGroup")

pre_save.connect(active_referral_offer_checks, sender=ReferralOffer, dispatch_uid='users.models.ReferralOffer')