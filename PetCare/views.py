from django.shortcuts import redirect, render

from .models import Customer, Profile
from django.contrib.auth import authenticate,login as auth_login
from .forms import UserForm

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
                    return redirect('customer/customer_home')
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
    return render(request,'customer/customer_details.html')
def customer_home(request):
    return render(request,'customer/customer_home.html')