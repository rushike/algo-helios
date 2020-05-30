from django.test import Client

from users.models import *

import random

def line(): print("\n" + "=" * 50 + "\n")

#Create a dummy user
user = AlgonautsUser.objects.create_user(
    first_name = "Test",
    last_name = "Algonauts",
    email = f"test{random.randint(1000, 100000)}.algonauts@gmail.com",
    contact_no = "8978689786",
    password = "okpasswordispassword",
)

print(f"User created : {user}")
line()

# initiating the dummy client
c = Client()


# Trying login through password
response = c.post('/accounts/login/', {'login': 'test.algonauts@gmail.com', 'password': 'okpasswordispassword'})
if response.status_code == 200: print(f"Response : {response}")
else : print(f"Login unsuccessful status_code : {response.status_code} \nResponse content : {response.content}")
line()

# Trying force login
c.force_login(user)
print(f"Force login : ")
line()


# Deleting Dummy User Created
res = AlgonautsUser.objects.filter(email = user.email).delete()
print(f"User deleted : {res}")
line()