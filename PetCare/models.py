from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    ROLE_CHOICES = (
        ('customer','Customer'),
        ('service_providers','Service Providers')
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

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    travel_distance = models.FloatField(null=True, blank=True)

    services = models.JSONField(null=True,blank=True)  # store selected services

    id_type = models.CharField(max_length=20, choices=ID_TYPE,null=True,blank=True)
    id_number = models.CharField(max_length=50,unique=True,null=True,blank=True,help_text="Government ID number")

    id_proof = models.FileField(upload_to='providers/id/',null=True,blank=True)

    grooming_certificate = models.FileField(upload_to='providers/certificates/',null=True,blank=True)
    vet_license = models.FileField(upload_to='providers/certificates/',null=True,blank=True)
    training_certificate = models.FileField(upload_to='providers/certificates/',null=True,blank=True)
    organization_registration = models.FileField(upload_to='providers/certificates/',null=True,blank=True)

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
class BlacklistedProvider(models.Model):
    full_name = models.CharField(max_length=100)

    id_type = models.CharField(max_length=20)
    id_number = models.CharField(max_length=50, unique=True)

    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    reason = models.TextField(default="Violation of platform policies")
    blacklisted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - BLACKLISTED"

class MyPet(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    pet_type = models.CharField(max_length=30,null=False,blank=False)
    pet_name = models.CharField(max_length=30,null=False,blank=False)
    breed = models.CharField(max_length=50,null=False,blank=False)
    age = models.PositiveIntegerField(null=False,blank=False)
    weight = models.PositiveIntegerField(null=False,blank=False)
    pet_photo = models.ImageField(upload_to='customers/pets/',null=True,blank=True)

    def __str__(self):
        return f"{self.customer}-{self.pet_name}"
    
class PetShop(models.Model):

    PET_TYPE_CHOICES = (
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
        ('Cats_and_Dogs','Cats and Dogs')
    )

    product_name = models.CharField(max_length=50, null=False, blank=False)
    product_category = models.CharField(max_length=50, null=False, blank=False)
    pet_type = models.CharField(max_length=50, choices=PET_TYPE_CHOICES)
    product_price = models.PositiveIntegerField(null=False, blank=False)
    stock_quantity = models.PositiveIntegerField(null=False, blank=False)
    product_description = models.TextField(max_length=100, null=False, blank=False)
    product_image = models.FileField(upload_to='products/', null=False, blank=False)

    def __str__(self):
        return self.product_name
    
# class Cart(models.Model):
#     customer = models.OneToOneField(Profile,on_delete=models.CASCADE)
class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    provider = models.ForeignKey(
        ServiceProvider,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    service_name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


# def __str__(self):
#     return f"{}"

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(PetShop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.product_price * self.quantity

    def __str__(self):
        return f"{self.customer.fullname} - {self.product.product_name}"

class ServiceBooking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    payment = models.OneToOneField(
        Payment,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('confirmed', 'Confirmed'),
            ('pending', 'Pending'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )

    def __str__(self):
        return f"{self.customer} - {self.service_name}"


class TimeSlot(models.Model):
    provider = models.ForeignKey(
        ServiceProvider,
        on_delete=models.CASCADE,
        related_name='timeslots'
    )

    service_name = models.CharField(max_length=100)  
    # example: "grooming", "dog walking"

    date = models.DateField()
    time = models.TimeField()   # ✅ SINGLE TIME (multiple rows = multiple times)

    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.service_name} | {self.date} | {self.time}"

from django.db import models
from django.contrib.auth.models import User

class VoiceCommand(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    command_text = models.TextField()
    intent = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.command_text[:50]
