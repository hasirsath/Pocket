from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')   # already logged in

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')   # SUCCESS → dashboard
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid credentials'
            })

    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validation
        if password != confirm_password:
            return render(request, 'accounts/register.html', {
                'error': 'Passwords do not match'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {
                'error': 'Username already exists'
            })

        # Create user safely
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Auto login after register (recommended)
        login(request, user)
        return redirect('dashboard')

    return render(request, 'accounts/register.html')
