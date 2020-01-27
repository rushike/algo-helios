# from .base import *
import os
if os.environ.get('DJANGO_DEVELOPMENT') is not None:
    from .base import * 
else : from .production import *