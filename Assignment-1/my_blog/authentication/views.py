from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse


# Create your views here.


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid username')
            print("\n\nHAHAHAHAHA\n\n")
            return redirect(reverse('login'))

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid password')
            return redirect(reverse('login'))
        else:
            login(request, user)
            return redirect(reverse('posts'))

    return render(request, 'authentication/login_page.html')


def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, "Username already taken!")
            return redirect(reverse('register'))

        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )

        # Set the user's password and save the user object
        user.set_password(password)
        user.save()

        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect(reverse('login'))

    # Render the registration page template (GET request)
    return render(request, 'authentication/register_page.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect(reverse('login'))
