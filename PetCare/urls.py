from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('learnmore/',views.learnmore,name='learnmore'),
    path('explore_services/',views.explore_services,name='explore_services'),
    path('signup/',views.register,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('customer_details/<int:customer_id>/',views.customer_details,name='customer_details'),
    path('customer_home/',views.customer_home,name='customer_home'),
]
