from django.shortcuts import render, redirect
from django.views import View
from .models import Donation, Category, Institution
from django.contrib.auth.models import User
from django.db.models import Sum
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout


class LandingPageView(View):
    def get(self, request):
        # quantity from Donation
        sum_of_bags = Donation.objects.aggregate(value=Sum('quantity'))
        institution_supported = Donation.objects.aggregate(value=Sum('institution'))
        ctx = {
            "sum_of_bags": sum_of_bags,
            "institution_supported": institution_supported
        }
        return render(request, "index.html", ctx)


class AddDonationView(View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {
            'categories': categories,
            'institutions': institutions,
        }
        return render(request, 'form.html', ctx)


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


class ProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            donations = Donation.objects.filter(user_id=user.id)
            ctx = {
                'user': user,
                'donations': donations
            }
            return render(request, 'user_profile.html', ctx)
