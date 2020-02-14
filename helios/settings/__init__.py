import os
print(os.environ.get('DJANGO_DEVELOPMENT'))
if os.environ.get('DJANGO_DEVELOPMENT') is not None:
    from .dev import * 
else : from .production import *