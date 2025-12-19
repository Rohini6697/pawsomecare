from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    ROLE_CHOICES = (
        # ('admin','Admin'),
        ('customer','Customer'),
        ('service_providers','Service Providers')
        # ('pet_walking','Petwalking'),
        # ('petsitting','Petsitting'),
        # ('petgrooming','Petgrooming'),
        # ('daycare','Daycare'),
        # ('boarding','Boarding'),
        # ('veterinary','Veterinary'),
        # ('training','Training')
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
    


class ServiceProvider(models.Model):
    PROVIDER_TYPE = (
        ('individual', 'Individual'),
        ('organization', 'Organization / Company'),
    )

    ID_TYPE = (
        ('aadhaar', 'Aadhaar'),
        ('pan', 'PAN'),
        ('passport', 'Passport'),
    )

    user = models.OneToOneField(Profile, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100,null=True,blank=True)
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    # profile_photo = models.ImageField(upload_to='providers/profile/', blank=True)

    provider_type = models.CharField(max_length=20, choices=PROVIDER_TYPE,null=True,blank=True)

    bio = models.TextField(null=True,blank=True)
    city = models.CharField(max_length=50,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    pincode = models.CharField(max_length=10,null=True,blank=True)

    latitude = models.CharField(max_length=50,null=True,blank=True)
    longitude = models.CharField(max_length=50,null=True,blank=True)

    travel_distance = models.PositiveIntegerField(null=True,blank=True)

    services = models.JSONField(null=True,blank=True)  # store selected services

    id_type = models.CharField(max_length=20, choices=ID_TYPE)
    id_proof = models.FileField(upload_to='providers/id/')

    grooming_certificate = models.FileField(upload_to='providers/certificates/', blank=True)
    vet_license = models.FileField(upload_to='providers/certificates/', blank=True)
    training_certificate = models.FileField(upload_to='providers/certificates/', blank=True)
    organization_registration = models.FileField(upload_to='providers/certificates/', blank=True)

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
