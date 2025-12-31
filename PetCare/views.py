from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import BlacklistedProvider, Customer, Profile, ServiceProvider
from django.contrib.auth import authenticate,login as auth_login,logout
from .forms import UserForm
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST


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

        if user is not None:
            auth_login(request, user)

            if user.is_superuser:
                return redirect('admin_home')

            role = user.profile.role

            if role == 'customer':
                try:
                    customer = user.profile.customer
                    return redirect('customer_home')
                except Customer.DoesNotExist:
                    return redirect('customer_details',customer_id=user.profile.id)
            elif role == 'service_providers':
                try:
                    provider = user.profile.serviceprovider
                except ServiceProvider.DoesNotExist:
                    return redirect('provider_details',provider_id=user.profile.id)
                if not provider.is_verified:
                    return redirect('provider_pending')
                else:
                    return redirect('provider_home')
            # other roles can be handled later
            else:
                return redirect('home')

        # ❌ login failed
        return render(request, 'signin.html', {
            'error': 'Invalid username or password'
        })

    # ✅ GET request (VERY IMPORTANT)
    return render(request, 'signin.html')  

def goback(request):
    logout(request)
    return redirect('signin')

# =========================================== Customer ==================================================
def customer_details(request,customer_id):
    profile = get_object_or_404(Profile,id = customer_id)
    customer,created = Customer.objects.get_or_create(customer=profile)
    if request.method == 'POST':
        customer.fullname = request.POST.get('fullname')
        customer.phone_number = request.POST.get('phone_number')
        customer.city = request.POST.get('city')
        customer.address = request.POST.get('address')
        customer.save()
        return redirect('customer_home')
    return render(request,'customer/customer_details.html',{'customer':customer})
def customer_home(request):
    return render(request,'customer/customer_home.html')
def my_pets(request):
    return render(request,'customer/my_pets.html')
def add_pets(request):
    return render(request,'customer/add_pets.html')
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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ServiceProvider, Profile

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
    return render(request,'provider/provider_home.html')
def provider_pending(request):
    return render(request,'provider/provider_pending.html')

# =========================================== Admin ==================================================
def admin_home(request):
    return render(request,'admin/admin_home.html')
def verify_providers(request):
    provider = ServiceProvider.objects.all()
    return render(request,'admin/verify_providers.html',{'providers':provider})
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
        None,  # uses DEFAULT_FROM_EMAIL
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
        None,
        [provider.user.user.email],
        fail_silently=False,
    )

    provider.user.user.delete()  # deletes everything
    provider.delete()
    return redirect('verify_providers')

def fire_provider(request,provider_id):
    provider = get_object_or_404(ServiceProvider,id = provider_id)
    if request.method == 'POST':
        BlacklistedProvider.objects.create(
            full_name=provider.full_name,
            id_type=provider.id_type,
            id_number=provider.id_number,
            phone_number=provider.phone_number,
            email=provider.user.user.email,
            # reason="Violation of platform policies"  
            reason = request.POST.get('reason')
            
        )

    # Disable provider
    provider.is_verified = False
    provider.save()
    return render('verify_providers')
def blacklisted_provider(request,provider_id):
    provider = ServiceProvider.objects.get(id = provider_id)

    return render(request,'admin/blacklisted_provider.html',{'provider':provider})