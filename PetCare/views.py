from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import BlacklistedProvider, Cart, Customer, MyPet, Payment, PetShop, Profile, ServiceBooking, ServiceProvider, TimeSlot
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

def service_bookings(request):
    customer = Customer.objects.get(customer=request.user.profile)

    bookings = ServiceBooking.objects.filter(
        customer=customer
    ).select_related("provider")

    return render(
        request,
        "customer/service_bookings.html",
        {"bookings": bookings}
    )

def shop(request):
    products = PetShop.objects.all()
    return render(request, 'customer/shop.html', {'products': products})

def cart(request):
    customer = get_object_or_404(Customer, customer=request.user.profile)

    cart_items = Cart.objects.filter(customer=customer)

    subtotal = 0
    for item in cart_items:
        subtotal += item.product.product_price * item.quantity

    delivery_charge = 99 if cart_items.exists() else 0
    total = subtotal + delivery_charge

    return render(request, "customer/cart.html", {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "total": total
    })

    # return render(request,'customer/cart.html')

def add_to_cart(request, product_id):
    product = get_object_or_404(PetShop, id=product_id)
    customer = get_object_or_404(Customer, customer=request.user.profile)

    cart_item, created = Cart.objects.get_or_create(
        customer=customer,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

def report(request):
    return render(request,'customer/report.html')
def new_booking(request):
    return render(request,'customer/new_booking.html')
@login_required
def update_pet(request, pet_id):
    profile = request.user.profile

    # ✅ get Customer from profile
    customer = get_object_or_404(Customer, customer=profile)

    # ✅ now query pet correctly
    pet = get_object_or_404(MyPet, id=pet_id, customer=customer)

    if request.method == 'POST':
        pet.pet_type = request.POST.get('pet_type')
        pet.pet_name = request.POST.get('pet_name')
        pet.breed = request.POST.get('pet_breed')
        pet.age = request.POST.get('age')
        pet.weight = request.POST.get('weight')

        if request.FILES.get('pet_photo'):
            pet.pet_photo = request.FILES.get('pet_photo')

        pet.save()
        return redirect('my_pets')

    return render(request, 'customer/update_pet.html', {'pet': pet})
def increase_qty(request, item_id):
    item = get_object_or_404(Cart, id=item_id)
    item.quantity += 1
    item.save()
    return redirect("cart")


def decrease_qty(request, item_id):
    item = get_object_or_404(Cart, id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect("cart")


def remove_from_cart(request, item_id):
    item = get_object_or_404(Cart, id=item_id)
    item.delete()
    return redirect("cart")
def create_cart_order(request):
    customer = get_object_or_404(Customer, customer=request.user.profile)
    cart_items = Cart.objects.filter(customer=customer)

    subtotal = 0
    for item in cart_items:
        subtotal += item.product.product_price * item.quantity

    delivery_charge = 99
    total_amount = subtotal + delivery_charge

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    order = client.order.create({
        "amount": total_amount * 100,  # rupees → paise
        "currency": "INR",
        "payment_capture": 1
    })

    return JsonResponse({
        "order_id": order["id"],
        "amount": total_amount * 100,
        "key": settings.RAZORPAY_KEY_ID
    })

from django.views.decorators.csrf import csrf_exempt

def create_service_order(request):
    if request.method == "POST":

        customer = Customer.objects.get(customer=request.user.profile)

        provider_id = request.POST.get("provider_id")
        service_name = request.POST.get("service")   # ✅ FIXED
        amount = int(request.POST.get("amount")) * 100

        provider = ServiceProvider.objects.get(id=provider_id)

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })

        Payment.objects.create(
            customer=customer,
            provider=provider,
            service_name=service_name,
            amount=amount // 100,
            razorpay_order_id=order["id"]
        )

        return JsonResponse({
            "order_id": order["id"],
            "key": settings.RAZORPAY_KEY_ID,   # ✅ FIXED
            "amount": amount
        })

import json
from django.views.decorators.csrf import csrf_exempt
from .models import ServiceBooking
from django.db import transaction
from .models import TimeSlot

@csrf_exempt
def verify_service_payment(request):
    if request.method == "POST":

        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_signature = request.POST.get("razorpay_signature")
        slot_id = request.POST.get("slot_id")

        payment = Payment.objects.get(
            razorpay_order_id=razorpay_order_id
        )

        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature = razorpay_signature
        payment.is_paid = True
        payment.save()

        # 🔒 LOCK SLOT (PREVENT DOUBLE BOOKING)
        with transaction.atomic():
            slot = TimeSlot.objects.select_for_update().get(id=slot_id)

            if not slot.is_available:
                return JsonResponse({"status": "already_booked"})

            slot.is_available = False
            slot.save()

        # ✅ CREATE SERVICE BOOKING
        ServiceBooking.objects.create(
            customer=payment.customer,
            provider=payment.provider,
            service_name=payment.service_name,
            amount=payment.amount,
            payment=payment
        )

        return JsonResponse({"status": "success"})

def refund_booking(request, booking_id):
    profile = request.user.profile

    if profile.role != "service_providers":
        return redirect("customer_home")

    booking = get_object_or_404(ServiceBooking, id=booking_id)
    payment = booking.payment

    # ❌ Safety checks
    if not payment.is_paid:
        messages.error(request, "Payment not completed")
        return redirect("provider_home")

    if booking.status == "cancelled":
        messages.warning(request, "Booking already cancelled")
        return redirect("provider_home")

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    try:
        with transaction.atomic():

            # 🔁 Razorpay refund
            client.payment.refund(
                payment.razorpay_payment_id,
                {
                    "amount": payment.amount * 100  # paise
                }
            )

            # 🔄 Update booking
            booking.status = "cancelled"
            booking.save()

            # 🔄 Free slot (best effort)
            TimeSlot.objects.filter(
                provider=booking.provider,
                service_name=booking.service_name,
                is_available=False
            ).update(is_available=True)

            messages.success(request, "Refund processed successfully")

    except Exception as e:
        messages.error(request, f"Refund failed: {str(e)}")

    return redirect("provider_home")



from django.shortcuts import render
from .models import ServiceProvider

def bookservice(request):
    providers = ServiceProvider.objects.filter(
        is_verified=True,
        user__role="service_providers"
    )

    service_keys = set()

    for provider in providers:
        if provider.services:

            # if services is a dictionary → use keys
            if isinstance(provider.services, dict):
                service_keys.update(provider.services.keys())

            # if services is a list → use values directly
            elif isinstance(provider.services, list):
                service_keys.update(provider.services)

    services = [
        {"key": key, "label": key.replace("_", " ").title()}
        for key in sorted(service_keys)
    ]

    return render(request, "customer/bookservice.html", {
        "services": services,
        "providers": providers
    })

def booknow(request,provider_id):
    provider = get_object_or_404(
        ServiceProvider,
        id=provider_id,
        is_verified=True
    )
    return render(request,'customer/booknow.html', {
        "provider": provider
    })

  
 

def slot_booking(request, provider_id):
    provider = get_object_or_404(ServiceProvider, id=provider_id)

    # ✅ get selected service from URL
    service = request.GET.get("service")
    if not service:
        return redirect("booknow", provider_id=provider_id)

    # ✅ get price from provider services
    price = provider.services.get(service)
    if not price:
        return redirect("booknow", provider_id=provider_id)

    # ✅ get available slots for this provider + service
    slots = TimeSlot.objects.filter(
        provider=provider,
        service_name=service,
        is_available=True
    ).order_by("date", "time")

    return render(request, "customer/slot_booking.html", {
        "provider": provider,
        "service": service,
        "price": price,
        "slots": slots
    })
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import ServiceBooking, ServiceProvider, Customer, TimeSlot

@login_required
def cash_on_service_booking(request, provider_id):
    if request.method != "POST":
        return redirect("bookservice")

    # 1️⃣ Check profile exists
    if not hasattr(request.user, "profile"):
        return HttpResponseForbidden("Profile not found")

    profile = request.user.profile

    # 2️⃣ Check role
    if profile.role != "customer":
        return HttpResponseForbidden("Only customers can book services")

    # 3️⃣ Check customer object
    try:
        customer = profile.customer
    except Customer.DoesNotExist:
        return HttpResponseForbidden("Customer profile missing")

    provider = get_object_or_404(ServiceProvider, id=provider_id)

    service = request.POST.get("service")
    amount = request.POST.get("amount")
    slot_id = request.POST.get("slot_id")

    # 4️⃣ Lock the slot
    slot = get_object_or_404(TimeSlot, id=slot_id, is_available=True)
    slot.is_available = False
    slot.save()

    # 5️⃣ Create booking (NO payment for COS)
    ServiceBooking.objects.create(
        customer=customer,
        provider=provider,
        service_name=service,
        amount=amount,
        status="confirmed"
    )

    return redirect("service_bookings")


# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import ServiceProvider, Profile
# ====================================== Provider ======================================
@login_required


def provider_details(request, provider_id):
    profile = get_object_or_404(Profile, id=provider_id)

    provider, created = ServiceProvider.objects.get_or_create(
        user=profile
    )

    if request.method == "POST":

        # BASIC DETAILS
        provider.full_name = request.POST.get("full_name")
        provider.phone_number = request.POST.get("phone_number")
        provider.provider_type = request.POST.get("provider_type")
        provider.bio = request.POST.get("bio")
        provider.city = request.POST.get("city")
        provider.address = request.POST.get("address")
        provider.pincode = request.POST.get("pincode")
        provider.travel_distance = request.POST.get("travel_distance")

        # ⭐ SERVICES + PRICE (IMPORTANT PART)
        selected_services = request.POST.getlist("services")
        services_data = {}

        for service in selected_services:
            price = request.POST.get(f"{service}_price")
            if price:
                services_data[service] = int(price)

        provider.services = services_data  # stored as JSON

        # ID DETAILS
        provider.id_type = request.POST.get("id_type")
        provider.id_number = request.POST.get("id_number")

        # FILES
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
def bookings(request, provider_id):
    profile = request.user.profile

    if profile.role != "service_providers":
        return redirect("customer_home")

    provider = ServiceProvider.objects.get(user=profile)

    bookings = ServiceBooking.objects.filter(
        provider=provider
    ).order_by("-booking_date")

    timeslots = TimeSlot.objects.filter(
        provider=provider,
        is_available=False   # booked slots only
    )

    return render(
        request,
        "provider/bookings.html",
        {
            "bookings": bookings,
            "timeslots": timeslots
        }
    )


import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def create_cart_order(request):
    if request.method == "POST":
        customer = Customer.objects.get(customer=request.user.profile)

        cart_items = Cart.objects.filter(customer=customer)
        if not cart_items.exists():
            return JsonResponse({"error": "Cart is empty"}, status=400)

        subtotal = sum(item.total_price() for item in cart_items)
        delivery_charge = 99
        total_amount = subtotal + delivery_charge

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        order = client.order.create({
            "amount": total_amount * 100,
            "currency": "INR",
            "payment_capture": 1
        })

        Payment.objects.create(
            customer=customer,
            provider=None,
            service_name="Cart Purchase",
            amount=total_amount,
            razorpay_order_id=order["id"],
            is_paid=False
        )

        return JsonResponse({
            "order_id": order["id"],
            "key": settings.RAZORPAY_KEY_ID,
            "amount": total_amount * 100
        })



@csrf_exempt
def verify_cart_payment(request):
    if request.method == "POST":

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        data = {
            "razorpay_order_id": request.POST.get("razorpay_order_id"),
            "razorpay_payment_id": request.POST.get("razorpay_payment_id"),
            "razorpay_signature": request.POST.get("razorpay_signature"),
        }

        try:
            client.utility.verify_payment_signature(data)

            payment = Payment.objects.get(
                razorpay_order_id=data["razorpay_order_id"]
            )

            payment.razorpay_payment_id = data["razorpay_payment_id"]
            payment.razorpay_signature = data["razorpay_signature"]
            payment.is_paid = True
            payment.save()

            # ✅ CLEAR CART
            Cart.objects.filter(customer=payment.customer).delete()

            return JsonResponse({"status": "success"})

        except Exception as e:
            print("Cart payment verify error:", e)
            return JsonResponse({"status": "failed"})

def services(request,provider_id):
    provider = request.user.profile.serviceprovider

    services = provider.services or {}  # JSON field
    timeslots = TimeSlot.objects.filter(provider=provider)

    if request.method == "POST":
        TimeSlot.objects.create(
            provider=provider,
            service_name=request.POST['service_name'],
            date=request.POST['date'],
            time=request.POST['time']
        )
    return render(request,'provider/services.html',{'services':services,'timeslots': timeslots})

def confirm_service(request, booking_id):
    booking = get_object_or_404(ServiceBooking, id=booking_id)

    # Safety checks
    if booking.status == "confirmed":
        messages.info(request, "Booking already confirmed")
        return redirect("provider_home")

    if booking.status == "cancelled":
        messages.error(request, "Cancelled booking cannot be confirmed")
        return redirect("provider_home")

    # ✅ Confirm booking
    booking.status = "confirmed"
    booking.save()

    # 📧 SEND EMAIL TO CUSTOMER
    customer_email = booking.customer.customer.user.email

    subject = "Your Service Booking is Confirmed 🐾"

    message = f"""
Hi {booking.customer.fullname},

Good news! 🎉

Your booking for **{booking.service_name.title()}** has been confirmed by the service provider.

Provider: {booking.provider.full_name}
Amount Paid: ₹{booking.amount}

📅 Please be available on the scheduled date and time.

Thank you for choosing Pawsome Care 🐶🐱




Regards,
Pawsome Care Team
"""

    if customer_email:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email],
            fail_silently=True
        )

    messages.success(request, "Service confirmed and email sent to customer")
    return redirect("provider_home")
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
def add_product(request):
    if request.method == 'POST':
        PetShop.objects.create(
            product_name = request.POST.get('name'),
            product_category = request.POST.get('category'),
            pet_type = request.POST.get('pet_type'),
            product_price = request.POST.get('price'),
            stock_quantity = request.POST.get('stock'),
            product_description = request.POST.get('description'),
            product_image = request.FILES.get('image'),
        )
        return redirect('view_products')

    return render(request,'admin/add_product.html')
def view_products(request):
    products = PetShop.objects.all()
    return render(request,'admin/view_products.html',{'products':products})
def update_products(request,product_id):
    product = PetShop.objects.get(id=product_id)
    if request.method == 'POST':
        product.product_name = request.POST.get('name')
        product.product_category = request.POST.get('category')
        product.product_price = request.POST.get('price')
        product.stock_quantity = request.POST.get('stock')
        product.product_category = request.POST.get('description')
        product.product_image = request.FILES.get('image')
        product.save()
        return redirect('view_products')
    return render(request,'admin/update_products.html',{'product':product})
def delete_products(request,product_id):
    product = get_object_or_404(PetShop,id=product_id)
    product.delete()
    return redirect('view_products')



# ------------------  Voice Assistant --------------------------------------
from django.http import JsonResponse
import json
from .ai_engine.intent_classifier import detect_intent

def ai_intent_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("command", "")

        intent, confidence = detect_intent(text)

        return JsonResponse({
            "text": text,
            "intent": intent,
            "confidence": round(confidence * 100, 2)
        })