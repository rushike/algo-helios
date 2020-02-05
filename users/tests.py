from django.test import TestCase

# Create your tests here.

for x in AlgonautsUser.objects.all():
    u = AlgonautsUser.objects.filter(id=x.id)
    u.update(referal_code=get_unique_referral_code())