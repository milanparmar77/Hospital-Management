import re

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from patient.models import Patient
from django.contrib import messages
from django.views.decorators.cache import never_cache

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if not re.fullmatch(r'[6-9]\d{9}', phone):
            messages.error(request, "Enter valid 10-digit phone number")
            return redirect('register')

        if not age:
            messages.error(request, "Age is required")
            return redirect('register')

        try:
            age = int(age)
        except ValueError:
            messages.error(request, "Age must be a number")
            return redirect('register')

        if age < 0 or age > 120:
            messages.error(request, "Age must be between 0 and 120")
            return redirect('register')

        if not gender:
            messages.error(request, "Please select a gender")
            return redirect('register')

        if Patient.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email = email,
                first_name=first_name,
                last_name=last_name
            )

           
            Patient.objects.create(
                user=user,
                age=age,
                gender=gender,
                phone=phone
            )

            messages.success(request, "Account created successfully")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('register')

    return render(request, 'accounts/register.html')

@never_cache
def user_login(request):

    if request.user.is_authenticated:
        if hasattr(request.user, 'patient'):
            return redirect('patient_home')
        elif hasattr(request.user, 'doctor'):
            return redirect('doctor_home')
        # else:
        #     return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if hasattr(user, 'patient'):
                return redirect('patient_home')

            elif hasattr(user, 'doctor'):
                return redirect('doctor_home')

            else:
                return redirect('admin_dashboard')

        response = render(request, 'accounts/login.html', {
            'error': 'Invalid username or password'
        })

    else:
        response = render(request, 'accounts/login.html')

    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    return response

@never_cache
def user_logout(request):
    logout(request)

    response = redirect('login')
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    return response

# @login_required
# def admin_dashboard(request):
#     return render(request, 'admin/dashboard.html')   