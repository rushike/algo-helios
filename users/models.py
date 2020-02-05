from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser, Group
from django.db import models
from django.core.validators import RegexValidator,MinLengthValidator
from django.utils import timezone
from django.db.models.fields import DateTimeField
from django.db.models.signals import post_save, pre_save

import datetime, random, string, time
from hashlib import md5
# from subscriptions.models import Plan
# random.seed(random.randint(0, 1000000))

"""
Constants or Functions
Calculates the default end date for user to removed
"""
REFERRAL_CODE_LEN = 6

def end_date():
		return datetime.datetime.now() + datetime.timedelta(weeks=52 * 100)

def get_unique_referral_code(seed = 0):
	# return '000000'
	# random.seed(md5(str(time.time).encode('utf8')))
	ref = random.sample(string.ascii_uppercase, REFERRAL_CODE_LEN)
	while AlgonautsUser.objects.filter(referral_code = ref).exists():
		ref = random.sample(string.ascii_uppercase, REFERRAL_CODE_LEN) #[random.choice(string.ascii_uppercase) for i in range(REFERRAL_CODE_LEN)]
	return ''.join(ref)	
def get_unique_referral_code_():
	return get_unique_referral_code(0)
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
		referral_code = get_unique_referral_code(email)
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
	referral_code = models.CharField(max_length=REFERRAL_CODE_LEN, validators=[MinLengthValidator(4)], default=get_unique_referral_code_)

	USERNAME_FIELD = 'email'
	EMAIL_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()

	# class Meta:
	# 	unique_together = ('referral_code',)

	def get_absolute_url(self):
		return "/users/%i/" % (self.pk)
	def join_to_group(self, group_id): # method add user(self) to the specific group with group_id 
		user_group_id = UserGroup.objects.get(id = group_id)
		mapper = UserGroupMapping.objects.create_user_group_mapping(user_profile_id= self, user_group_id=user_group_id, delta_period=4, group_admin= False)
		return mapper

	def get_user_subs_plans(self):
		iGroupType = UserGroupType.objects.get(type_name = 'individual') # get the individual object from moddles
		eGroupType = UserGroupType.objects.exclude(type_name = 'individual') # get rest group types available from model
		#one user linked with multiple groups
		user_all_groups = UserGroupMapping.objects.all().values('user_profile_id', 'user_group_id', 'user_group_id__user_group_type_id').values('user_group_id__user_group_type_id')
		indivdual =	user_all_groups.filter(user_profile_id=self, user_group_id__user_group_type_id = iGroupType).values('user_group_id__user_group_type_id')
		group = user_all_groups.filter(user_profile_id=self, user_group_id__user_group_type_id__in = eGroupType) # filter out all groups of profile with non individual group type 
		
		indivdual_plans = Plan.objects.filter(user_group_type_id__in = indivdual)
		group_plans = Plan.objects.filter(user_group_type_id__in = group)		

		raise InterruptedError("Checking variable values")
		

		pass

	def __str__(self):
		return "_".join((str(self.email)).split("@"))

class UserGroupType(models.Model):
	type_name = models.CharField(max_length=128)
	max_members = models.IntegerField(default=1)
	min_members = models.IntegerField(default=1)
	standard_group = models.BooleanField(default=True, blank=True)
	objects = models.Manager()
	class Meta:
		unique_together = ('type_name',)

	def __str__(self):
		return str(self.type_name)


class UserGroupManager(models.Manager):
	def create_user_group(self, user_group_type_id, admin):
		try : #can validate if any restrictions, returns None if, user_group with user_group_type, admin already present
			user_group = self.model(user_group_type_id = user_group_type_id, registration_time = datetime.datetime.now, admin = admin)
			user_group.save(using=self._db)
			return user_group
		except:
			return 


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
		raise EnvironmentError
		pass
	pass

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
	class Meta:
		unique_together = ('referred_by', 'referred_to',)
	def __str__(self):
		return str(self.referral_code)

class UserGroupMappingManager(models.Manager):
	def create_user_group_mapping(self, user_profile_id, user_group_id, delta_period, group_admin): # delta period in number of weeks
		if user_group_id is None: return # if group is not form due to some err, don't add user_group_mapping 
		mems = UserGroupMapping.objects.filter(user_group_id = user_group_id).count() # neccessary to check how many members currently present in group
		unq = UserGroupMapping.objects.filter(user_group_id = user_group_id, user_profile_id = user_profile_id).exists() # to check if duplicate entry 
		if unq: return # allow one user to be admin of only one user group of particular type
		
		mzx = UserGroupType.objects.filter(type_name = user_group_id.user_group_type_id)[0].max_members # checks the maximum number allowed by particular group
		if mzx < mems: return # do not add more than max number specified
		
		mapper = self.create(
				user_group_id = user_group_id, 
				user_profile_id = user_profile_id, 
				time_added = datetime.datetime.now(),
				time_removed = datetime.datetime.now() + datetime.timedelta(weeks=4),
				group_admin = True)
		mapper.save(using = self._db)
		return mapper
	pass

class UserGroupMapping(models.Model):
	user_group_id = models.ForeignKey(UserGroup, on_delete=models.CASCADE, related_name="ugm_user_group_id")
	user_profile_id = models.ForeignKey(AlgonautsUser, on_delete= models.CASCADE, related_name="ugm_user_profile_id")
	time_added = models.DateTimeField(auto_now=True)
	time_removed = models.DateTimeField(default = end_date)
	group_admin = models.BooleanField(default=False)
	objects = UserGroupMappingManager()
	@property
	def is_present(self):
		if datetime.datetime.now > self.time_removed : 
			return True
		return False

	@property
	def get_user_group_type(self):
		return self.user_group_id.user_group_type_id

	def __str__(self):
		return "#".join([str(self.user_profile_id) , str(self.user_group_id)])
  
# Code to add permission to group 
def create_individual_user_group(sender, instance, **kwargs):
	indiv = UserGroupType.objects.get_or_create(type_name='individual')[0]

	group = UserGroup.objects.create_user_group(user_group_type_id=indiv, admin = instance)
	# group.save()
	if group is None : return
	group_map = UserGroupMapping.objects.create_user_group_mapping(user_group_id = group, user_profile_id = instance, delta_period= 4, group_admin = True)
	# group_map.save()
	return

def create_ug_mapping(sender, instance, **kwargs):
	group_map = UserGroupMapping.objects.create_user_group_mapping(user_group_id = instance, user_profile_id = instance.admin, delta_period= 4, group_admin = True)
	# group_map.save()
	return

def active_referral_offer_checks(sender, instance, **kwargs):
	# ReferralOffer.
	offer_active = instance.offer_active
	if offer_active:
			ReferralOffer.objects.filter(offer_active = True).update(offer_active = False)
			
# pass

# DB Signals 
post_save.connect(create_individual_user_group, sender=AlgonautsUser, dispatch_uid="users.models.AlgonautsUser") # to create users individual group after user creation

post_save.connect(create_ug_mapping, sender=UserGroup, dispatch_uid="users.models.UserGroup")

pre_save.connect(active_referral_offer_checks, sender=ReferralOffer, dispatch_uid='users.models.ReferralOffer')