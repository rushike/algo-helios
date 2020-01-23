from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser, Group
from django.db import models
from django.core.validators import RegexValidator
# from unixtimestampfield.fields import UnixTimeStampField
from django.utils import timezone
import datetime
from django.db.models.fields import DateTimeField


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
                # assume that the value is a timestamp if it is not a datetime
                value = datetime.datetime.fromtimestamp(int(value))
                # an exception might be better than an assumption
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
	# id = models.IntegerField(primary_key=True)
	first_name = models.CharField(max_length=64)
	last_name = models.CharField(max_length=64)
	email = models.EmailField(max_length=254, unique=True)
	contact_no = models.CharField(max_length=10) #RegexValidator(regex = r'^[0-9]*$')
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	last_login = models.DateTimeField(null=True, blank=True)
	date_joined = models.DateTimeField(auto_now_add=True)


	USERNAME_FIELD = 'email'
	EMAIL_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()

	def get_absolute_url(self):
		return "/users/%i/" % (self.pk)

class UserGroupType(models.Model):
	# id = models.IntegerField(primary_key=True)
	type_name = models.CharField(max_length=128)
	max_members = models.IntegerField()
	min_members = models.IntegerField()
	standard_group = models.CharField(max_length=128)

class UserGroup(models.Model):
	# id = models.IntegerField(primary_key=True, )
	user_group_type_id = models.ForeignKey(UserGroupType, on_delete = models.CASCADE)
	members = models.ManyToManyField(
		AlgonautsUser,
		through='UserGroupMapping',
		through_fields=('user_group_id', 'user_profile_id'),
	)
	registration_time = models.DateTimeField(auto_now=True)


class UserGroupMapping(models.Model):
	# id = models.IntegerField(primary_key=True)
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



class ReferralOffer(models.Model):
    offer_name = models.CharField(max_length=100)


class Referrals(models.Model):
    referral_code = models.IntegerField()
    referred_by = models.ForeignKey(AlgonautsUser, on_delete=models.CASCADE, related_name='by') 
    referred_to = models.ForeignKey(AlgonautsUser, on_delete=models.CASCADE, related_name='to') 
    referral_time = models.DateTimeField()
    referral_offer_id = models.ForeignKey(ReferralOffer, on_delete=models.CASCADE)




