from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import BlacklistedProvider, Customer, MyPet, Profile, ServiceProvider
from django.contrib.auth import authenticate,login as auth_login,logout
from .forms import UserForm
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings


# Create your views here.
def home(request):
    return render(request,'home.html')
def learnmore(request):
    return render(request,'learnmore.html')
def explore_services(request):
    return render(request,'explore_services.html')
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            Profile.objects.create(user=user,role = form.cleaned_data['role'])
            return redirect('signin')
        
    else:
        form = UserForm()

    return render(request,'signup.html',{'form':form})

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)

            if user.is_superuser:
                return redirect('admin_home')

            # Always get the profile FIRST
            profile, created = Profile.objects.get_or_create(user=user)

            role = profile.role

            if role == 'customer':
                try:
                    customer = profile.customer  # OneToOne access
                    return redirect('customer_home')
                except Customer.DoesNotExist:
                    return redirect('customer_details', profile_id=profile.id)

            elif role == 'service_providers':
                try:
                    provider = profile.serviceprovider
                except ServiceProvider.DoesNotExist:
                    return redirect('provider_details', provider_id=profile.id)

                if not provider.is_verified:
                    return redirect('provider_pending')

                return redirect('provider_home')

            return redirect('home')

        return render(request, 'signin.html', {'error': 'Invalid username or password'})

    return render(request, 'signin.html')


def goback(request):
    logout(request)
    return redirect('signin')

# =========================================== Customer ==================================================
def customer_details(request,profile_id):
    profile = get_object_or_404(Profile,id = profile_id)
    customer,created = Customer.objects.get_or_create(customer=profile)
    if request.method == 'POST':
        customer.fullname = request.POST.get('fullname')
        customer.phone_number = request.POST.get('phone_number')
        customer.city = request.POST.get('city')
        customer.address = request.POST.get('address')
        customer.save()
        return redirect('customer_home')
    return render(
        request,
        'customer/customer_details.html',
        {
            'profile': profile,     # ✅ REQUIRED
            'customer': customer
        }
    )
def customer_home(request):
    
    return render(request,'customer/customer_home.html')
def my_pets(request):
    profile = request.user.profile
    customer = get_object_or_404(Customer, customer=profile)

    pets = MyPet.objects.filter(customer=customer)  
    return render(request,'customer/my_pets.html',{'pets':pets})
def add_pets(request):
    customer = get_object_or_404(Customer, customer=request.user.profile)

    if request.method == 'POST':
        MyPet.objects.create(
            customer=customer,
            pet_type=request.POST.get('pet_type'),
            pet_name=request.POST.get('pet_name'),
            breed=request.POST.get('pet_breed'),
            age=request.POST.get('age') or None,
            weight=request.POST.get('weight') or None,
            pet_photo=request.FILES.get('photo')
        )

        return redirect('my_pets')

    return render(request, 'customer/add_pets.html')

def bookings(request):
    return render(request,'customer/bookings.html')
def shop(request):
    return render(request,'customer/shop.html')
def cart(request):
    return render(request,'customer/cart.html')
def report(request):
    return render(request,'customer/report.html')
def new_booking(request):
    return render(request,'customer/new_booking.html')
def update_pet(request):
    return render(request,'customer/update_pet.html')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ServiceProvider, Profile
# ====================================== Provider ======================================
@login_required
def provider_details(request, provider_id):
    profile = get_object_or_404(Profile, id=provider_id)

    provider, created = ServiceProvider.objects.get_or_create(
        user=profile
    )

    if request.method == "POST":

        provider.full_name = request.POST.get("full_name")
        provider.phone_number = request.POST.get("phone_number")
        provider.provider_type = request.POST.get("provider_type")
        provider.bio = request.POST.get("bio")
        provider.city = request.POST.get("city")
        provider.address = request.POST.get("address")
        provider.pincode = request.POST.get("pincode")
        provider.travel_distance = request.POST.get("travel_distance")

        # Services (checkboxes)
        provider.services = request.POST.getlist("services")
        provider.id_type = request.POST.get("id_type")
        provider.id_number = request.POST.get('id_number')

        # Files
        if request.FILES.get("id_proof"):
            provider.id_proof = request.FILES.get("id_proof")

        if request.FILES.get("grooming_certificate"):
            provider.grooming_certificate = request.FILES.get("grooming_certificate")

        if request.FILES.get("vet_license"):
            provider.vet_license = request.FILES.get("vet_license")

        if request.FILES.get("training_certificate"):
            provider.training_certificate = request.FILES.get("training_certificate")

        if request.FILES.get("organization_registration"):
            provider.organization_registration = request.FILES.get("organization_registration")

        provider.save()

        messages.success(request, "Profile submitted successfully!")
        return redirect("provider_pending")

    return render(
        request,
        "provider/provider_details.html",
        {"provider": provider}
    )


def provider_home(request):
    provider = request.user.profile.serviceprovider
    return render(request,'provider/provider_home.html',{'provider':provider})
def provider_pending(request):
    return render(request,'provider/provider_pending.html')
def edit_provider_profile(request,provider_id):
    provider = get_object_or_404(ServiceProvider, id=provider_id)

    return render(request,'provider/edit_provider_profile.html',{'provider':provider})
def bookings(request,provider_id):
    return render(request,'provider/bookings.html')





# =========================================== Admin ==================================================
def admin_home(request):
    return render(request,'admin/admin_home.html')
def verify_providers(request):
    provider = ServiceProvider.objects.all()
    blacklisted = list(
        BlacklistedProvider.objects.values('id_number', 'email', 'phone_number')
    )
    return render(request,'admin/verify_providers.html',{'providers':provider,
                                                         'blacklisted':blacklisted})
def accept_providers(request,provider_id):
    provider = ServiceProvider.objects.get(id = provider_id)
    provider.is_verified =True
    provider.save()
      # 📧 Send email
    subject = 'Your Service Provider Account Has Been Verified'
    message = f"""
    Hello {provider.full_name},

    Congratulations! 🎉

    Your service provider account has been successfully verified.
    You can now log in and start using our platform.

    Best regards,
    Pawsome Care Team
    """
    send_mail(
    subject,
    message,
    settings.EMAIL_HOST_USER,
    [provider.user.user.email],
    fail_silently=False,
)
    return redirect('verify_providers')
def reject_providers(request,provider_id):
    provider = ServiceProvider.objects.get(id = provider_id)
    # 📧 Email before deleting
    subject = 'Service Provider Application Rejected'
    message = f"""
    Hello {provider.full_name},

    We regret to inform you that your service provider application
    has been rejected.

    For further details, please contact support.

    Regards,
    Pawsome Care Team
    """
    send_mail(
    subject,
    message,
    settings.EMAIL_HOST_USER,
    [provider.user.user.email],
    fail_silently=False,
)

    provider.user.user.delete()  # deletes everything
    provider.delete()
    return redirect('verify_providers')

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def fire_provider(request, provider_id):
    provider = get_object_or_404(ServiceProvider, id=provider_id)

    if request.method == 'POST':
        reason = request.POST.get('reason') or "Violation of platform policies"

        provider_email = provider.user.user.email
        provider_name = provider.full_name

        # ⛔ Prevent duplicate blacklist
        if BlacklistedProvider.objects.filter(id_number=provider.id_number).exists():
            messages.error(request, "This provider is already blacklisted.")
            return redirect('provider_manage')

        # Add to blacklist
        BlacklistedProvider.objects.create(
            full_name=provider.full_name,
            id_type=provider.id_type,
            id_number=provider.id_number,
            phone_number=provider.phone_number,
            email=provider_email,
            reason=reason
        )

        # Disable & delete
        provider.is_verified = False
        provider.save()
        provider.user.delete()

        # Email
        subject = "Account Deactivation – Pawsome Care"
        message = f"""
Dear {provider_name},

Your service provider account on Pawsome Care has been deactivated.

Reason:
{reason}

If you believe this action was taken in error, please contact our support team.

Regards,
Pawsome Care Admin Team
"""

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [provider_email],
            fail_silently=False,
        )

    return redirect('provider_manage')


def blacklist_provider(request,provider_id):
    provider = ServiceProvider.objects.get(id = provider_id)

    return render(request,'admin/blacklisted_provider.html',{'provider':provider})
def provider_manage(request):
    providers = ServiceProvider.objects.filter(is_verified = True)
    return render(request,'admin/provider_manage.html',{'providers':providers})
def blacklist(request):
    providers = BlacklistedProvider.objects.all()
    return render(request,'admin/blacklist.html',{'providers':providers})