from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('learnmore/',views.learnmore,name='learnmore'),
    path('explore_services/',views.explore_services,name='explore_services'),
    path('signup/',views.register,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('goback/',views.goback,name='goback'),


    path('customer_details/<int:profile_id>/',views.customer_details,name='customer_details'),
    path('customer_home/',views.customer_home,name='customer_home'),
    path('my_pets/',views.my_pets,name='my_pets'),
    path('add_pets/',views.add_pets,name='add_pets'),
    path('service_bookings/',views.service_bookings,name='service_bookings'),
    path('shop/',views.shop,name='shop'),
    path('cart/',views.cart,name='cart'),
    path('report/',views.report,name='report'),
    path('new_booking/',views.new_booking,name='new_booking'),
    path('update_pet/<int:pet_id>/',views.update_pet,name='update_pet'),
    path('bookservice/',views.bookservice,name='bookservice'),



    path('provider_details/<int:provider_id>/',views.provider_details,name='provider_details'),
    path('provider_home/',views.provider_home,name='provider_home'),
    path('provider_pending/',views.provider_pending,name='provider_pending'),
    path('edit_provider_profile/<int:provider_id>/',views.edit_provider_profile,name='edit_provider_profile'),
    path('bookings/<int:provider_id>/',views.bookings,name='bookings'),
    
    


    path('admin_home/',views.admin_home,name='admin_home'),
    path('verify_providers/',views.verify_providers,name='verify_providers'),
    path('accept_providers/<int:provider_id>',views.accept_providers,name='accept_providers'),
    path('reject_providers/<int:provider_id>',views.reject_providers,name='reject_providers'),
    path('blacklist_provider/<int:provider_id>',views.blacklist_provider,name='blacklist_provider'),
    path('fire_provider/<int:provider_id>',views.fire_provider,name='fire_provider'),
    path('provider_manage/',views.provider_manage,name='provider_manage'),
    path('blacklist/',views.blacklist,name='blacklist'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
