from django.db import models

class META:
    key = models.CharField(max_length=64, primary_key=True)
    value = models.CharField(max_length=8192)
