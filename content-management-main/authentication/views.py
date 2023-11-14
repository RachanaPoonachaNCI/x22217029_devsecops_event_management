from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from . import models


# Create your views here.
@csrf_exempt
def login_api(request):
    if request.method == "POST":
        print(request.POST)
        try:
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                return redirect("/auth/")
        except Exception as e:
            print("Login error:", e)
            return redirect("/auth/")
    else:
        return redirect("/auth/")


@csrf_exempt
def signup_api(request):
    if request.method == "POST":
        print(request.POST)
        email = request.POST["email"]
        password = request.POST["password"]
        cpassword = request.POST["cpassword"]
        name = request.POST["name"]
        if password != cpassword:
            return redirect("/auth")
        user = User.objects.filter(username=email).first()
        if user:
            return redirect("/auth/")
        try:
            # Create a new user
            user = User.objects.create_user(username=email, password=password)
            new = models.user(name=name, email=email)
            new.save()
            login(request, user)
            return redirect("/")
        except Exception as e:
            print("Signup error:", e)
            return redirect("/auth/")
    else:
        return redirect("/auth/")


@csrf_exempt
def authentication(request):
    if request.method == "GET":
        return render(
            request, "authform.html", context={"message": "Success"}, status=201
        )


@login_required(login_url="/auth/")
def logout_api(request):
    logout(request)
    return redirect("/auth/")
