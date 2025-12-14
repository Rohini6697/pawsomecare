from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    ROLE_CHOICES = (
        # ('admin','Admin'),
        ('customer','Customer'),
        ('pet_walking','Petwalking'),
        ('petsitting','Petsitting'),
        ('petgrooming','Petgrooming'),
        ('daycare','Daycare'),
        ('boarding','Boarding'),
        ('veterinary','Veterinary'),
        ('training','Training')
    )
    role = models.CharField(max_length=50,choices=ROLE_CHOICES,default='customer')

    def __str__(self):
        return f"{self.user.username}"
    
class Customer(models.Model):
    customer = models.OneToOneField(Profile,on_delete=models.CASCADE)
    fullname = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=70)

    def __str__(self):
        return f"{self.fullname}"