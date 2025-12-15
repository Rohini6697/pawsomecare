from django.shortcuts import redirect, render

from .models import Customer, Profile
from django.contrib.auth import authenticate,login as auth_login
from .forms import UserForm
from django.shortcuts import get_object_or_404


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
                return redirect('admindashboard')

            role = user.profile.role

            if role == 'customer':
                try:
                    customer = user.profile.customer
                    return redirect('customer_home')
                except Customer.DoesNotExist:
                    return redirect('customer_details',customer_id=user.profile.id)

            # other roles can be handled later
            return redirect('home')

        # ❌ login failed
        return render(request, 'signin.html', {
            'error': 'Invalid username or password'
        })

    # ✅ GET request (VERY IMPORTANT)
    return render(request, 'signin.html')  
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
def pet_food(request):
    return render(request,'customer/pet_food.html')
