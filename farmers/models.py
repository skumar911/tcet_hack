from django.db import models

# Create your models here.
class Farmer(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=500)
    contact=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    village=models.CharField(max_length=1000)
    grain=models.CharField(max_length=100)
    pic_url=models.CharField(max_length=100)



class Experts(models.Model):
    e_password=models.CharField(max_length=100)
    e_uname=models.CharField(max_length=100)

class Enquiry(models.Model):
    farmer_name=models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    desc=models.CharField(max_length=500)
    status=models.CharField(max_length=100)
    solution=models.CharField(max_length=500)


class Chat(models.Model):
    fromm=models.CharField(max_length=100)
    to=models.CharField(max_length=100)
    msg=models.CharField(max_length=1000)
    current_time=models.DateTimeField(auto_now_add=True)

class AddYield(models.Model):
    f_uname=models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    year=models.CharField(max_length=100)
    yieldd=models.CharField(max_length=100)
