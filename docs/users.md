# Users App
App handles responsibilty for user authentication and group formation and managment.

Users [Allauth][alluth] library for user authentication and social app login

## Social App 
Supported **Facebook** and **Google**. 
These app need to set through **`/admin`** panel. Only admin users can access and edit these.


## Dashboard
Includes functions for :
- User Info
- Downloading Invoices
- Referal Offer
- Manage Subscriptions
    - Renew
    - Terminate
- Group Management
    - Add group members
    - Remove group members    

## References : 
- allauth : https://django-allauth.readthedocs.io/en/latest/overview.html
- allauth-git : https://github.com/pennersr/django-allauth 

[static]: ./static.md
[allauth]: https://django-allauth.readthedocs.io/en/latest/overview.html
[allauth-git]: https://github.com/pennersr/django-allauth