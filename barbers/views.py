from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from barbers.models import Appointment
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

def index(request):
    return render(request, "barbers/index.html")

@login_required
def appointment(request):
    if request.method == 'POST':
        appointment = Appointment.objects.create(
            fname=request.POST.get('fname'),
            lname=request.POST.get('lname'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            contact=request.POST.get('contact'),
            barber=request.POST.get('barber'),
            date=request.POST.get('myDate'),
            time=request.POST.get('time'),
            comment=request.POST.get('comment'),
        )

        if appointment:
            context = {
                "client": appointment,
            }
            messages.success(request, 'Your appointment has been booked successfully.')
            return redirect('index')
        else:
            messages.error(request, 'Invalid input. Please try again.')
            return redirect('appointment')
    else:
        return render(request, "barbers/appointment.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            messages.error(request, 'Both username and password are required.')
            return redirect('appointment')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'You have logged in successfully.')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username and/or password.')
            return redirect('appointment')
    else:
        
        return render(request, "barbers/login.html")

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        if not username or not password or not first_name or not last_name or not email:
            messages.error(request, 'All fields must be completed.')
            return redirect('appointment')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('appointment')
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        login(request, user)
        messages.success(request, 'You have registered and logged in successfully.')
        return redirect('index')
    else:
        return render(request, "barbers/register.html")

