from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import generics

from .models import UserProfile
from .serializers import UserProfileSerializer


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username.')
            return redirect('/authentication/login/')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/authentication/login/')
        else:
            login(request, user)

            # Redirect to 2FA setup if the user has no registered TOTP device
            if not TOTPDevice.objects.filter(user=user, confirmed=True).exists():
                return redirect('/account/two_factor/setup/')

            return redirect('/home/')

    return render(request, 'login.html')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, "Username already taken!")
            return redirect('/authentication/register/')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )

        user.set_password(password)
        user.save()

        messages.info(request, "Account created Successfully!")
        return redirect('/authentication/register/')

    return render(request, 'register.html')


class UserProfileListView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
