from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField
    pnumber = models.CharField
    email = models.EmailField(unique=True)
    reg_date = models.DateTimeField(auto_now_add=True)