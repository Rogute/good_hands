from django.shortcuts import render, redirect
from django.views import View
from .models import Donation
from django.contrib.auth.models import User
from django.db.models import Sum
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout


class LandingPageView(View):
    def get(self, request):
        # quantity from Donation
        sum_of_bags = Donation.objects.aggregate(Sum('quantity'))
        ctx = {
            "sum_of_bags": sum_of_bags
        }
        return render(request, "index.html", ctx)


class AddDonationView(View):
    def get(self, request):
        return render(request, "form.html")


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
        return render(request, "login.html", {"form": form})


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect("index")


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password1"]
            user = User.objects.create(
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                username=form.cleaned_data["email"]
            )
            user.set_password(password)
            user.save()

            return redirect("login")
        return render(request, "register.html", {"form": form})
