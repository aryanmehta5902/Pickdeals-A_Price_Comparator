from django.db import models
from django.forms import Textarea
# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=16,primary_key=True)
    password = models.CharField(max_length=10)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    genders = [('M','MALE'),('F','FEMALE'),('O','OTHERS')]
    gender = models.CharField(max_length=1,choices=genders)
    mobile_no = models.CharField(max_length=10)
    email = models.EmailField() 
    dob = models.DateField(help_text="Please Enter Date in format YYYY-MM-DD")
    address = models.TextField() 


class Product(models.Model):
    user = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    value = models.IntegerField()