from django.test import TestCase
from django.test.client import RequestFactory

from users.models import AlgonautsUser, UserGroupType
from subscriptions.models import Order, Payment, Subscription
from worker.views import mercury
import random

# Create your tests here.
class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = user = AlgonautsUser.objects.create_user(
                    first_name = "Test",
                    last_name = "Algonauts",
                    email = f"test{random.randint(1000, 1000000)}.algonauts@gmail.com",
                    contact_no = "8978689786",
                    password = "okpasswordispassword",
                )
    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/worker/mercury')
        request.user = self.user
        print(f"Request object by factory : {request}")
        # Giving request to mercury 
        response = mercury(request)
        print(f"Response Obtain : {response}")
        # self.assertEqual(response.status_code, 200)
    def delete(self):
        self.user.delete()


# tester = SimpleTest()
# tester.setUp()
# tester.test_details()
# tester.delete() 

