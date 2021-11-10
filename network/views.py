from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .models import User, Post


def home(request):
    posts = Post.objects.order_by("-modified")
    return render(request, "network/home.html", {"posts": posts})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            # Valid user
            login(request, user)
            return redirect("home")
        else:
            # Wrong credentials
            return render(request, "network/login.html", {"message": "Invalid Credentials!"})
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        if not (username and email and password and confirmation):
            return render(request, "network/register.html", {"message": "Enter all fields"})

        if confirmation != password:
            return render(request, "network/register.html", {"message": "Confirmation password not matched!"})

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
        except IntegrityError:
            return render(request, "network/register.html", {"message": "Username already exists in system!"})

        login(request, user)
        return redirect("home")
    else:
        return render(request, "network/register.html")
