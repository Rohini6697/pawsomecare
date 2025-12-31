from .models import BlacklistedProvider, Customer, Profile, ServiceProvider
from django.contrib import admin

# Register your models here.
admin.site.register(Profile)
admin.site.register(Customer)
admin.site.register(ServiceProvider)
admin.site.register(BlacklistedProvider)
