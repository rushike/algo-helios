from django.test import TestCase
from django.test.client import RequestFactory

from django.test import TestCase
from channels.testing import WebsocketCommunicator


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
        self.assertEqual(response.status_code, 200)
    def delete(self):
        self.user.delete()


class MercuryTest(TestCase):
    def setUp(self, maxc = 10):
        import random
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.users = []
        self.maxc = maxc
        for i in range(maxc):
            rad = str(random.randint(i * 100, i + random.randint(0, 89898) * 100000))
            user = AlgonautsUser.objects.create_user(
                        first_name = "Test" + rad,
                        last_name = "Algonauts",
                        email = f"test{rad}.algonauts@gmail.com",
                        contact_no = "8978689786",
                        password = "okpasswordispassword",
                    )
            self.users.append(user)
            payment = Payment.objects.all().last()
            Subscription.objects.create_subscription(
                user = user,
                group_type = 'individual',
                plan_type = 'Premium',
                plan_name = 'Mercury',
                period = 'monthly',
                payment_id = payment,
            )
    def test_concurrent(self):
        for i in range(self.maxc):
            request = self.factory.get('https://dev.algonauts.in/worker/mercury')
            request.user = self.users[i]
            print(f"Request object by factory : {request}")
            # Giving request to mercury 
            response = mercury(request)
            print(f"Response Obtain : {response}, len : {len(str(response.content))}")
            self.assertEqual(response.status_code, 200)
    def delete(self):
        for i in range(self.maxc):
            self.users[i].delete()

# class WebsocketTestCase(TestCase):
#     @async_test
#     async def test_auth(self):
#         user = User.objects.create_user(**user_kwargs)
#         self.client.login(username=user.username, password=password)

#         headers = [(b'origin', b'...'), (b'cookie', self.client.cookies.output(header='', sep='; ').encode())]
#         communicator = WebsocketCommunicator(application, '/endpoint/', headers)
#         connected, _ = await communicator.connect()
#         self.assertTrue(connected)
#         self.assertEquals(communicator.instance.scope['user'], user)
#         await communicator.disconnect()

tester = SimpleTest()
tester.setUp()
tester.test_details()
tester.delete() 

# multitest = MercuryTest()
# multitest.setUp(10)
# multitest.test_concurrent()
# multitest.delete()
