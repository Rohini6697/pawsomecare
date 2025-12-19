from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('learnmore/',views.learnmore,name='learnmore'),
    path('explore_services/',views.explore_services,name='explore_services'),
    path('signup/',views.register,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('goback/',views.goback,name='goback'),
    path('customer_details/<int:customer_id>/',views.customer_details,name='customer_details'),
    path('customer_home/',views.customer_home,name='customer_home'),
    path('my_pets/',views.my_pets,name='my_pets'),
    path('add_pets/',views.add_pets,name='add_pets'),
    path('bookings/',views.bookings,name='bookings'),
    path('shop/',views.shop,name='shop'),
    path('cart/',views.cart,name='cart'),
    path('report/',views.report,name='report'),
    path('new_booking/',views.new_booking,name='new_booking'),
    path('provider_details/<int:provider_id>/',views.provider_details,name='provider_details'),
    path('provider_home/',views.provider_home,name='provider_home'),
    path('provider_pending/',views.provider_pending,name='provider_pending'),
    path('admin_home/',views.admin_home,name='admin_home'),
]
