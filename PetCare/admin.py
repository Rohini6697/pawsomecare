from .models import BlacklistedProvider, Cart, Customer, MyPet, Payment, PetShop, Profile, ServiceBooking, ServiceProvider
from django.contrib import admin

# Register your models here.
admin.site.register(Profile)
admin.site.register(Customer)
admin.site.register(ServiceProvider)
admin.site.register(MyPet)
admin.site.register(PetShop)
admin.site.register(Payment)
admin.site.register(Cart)
admin.site.register(ServiceBooking)

