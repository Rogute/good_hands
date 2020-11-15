from django.shortcuts import render, redirect
from django.views import View
from .models import Donation
from django.contrib.auth.models import User
from django.db.models import Sum
from .forms import RegisterForm


class LandingPage(View):
    def get(self, request):
        # quantity from Donation
        sum_of_bags = Donation.objects.aggregate(Sum('quantity'))
        ctx = {
            "sum_of_bags": sum_of_bags
        }
        return render(request, "index.html", ctx)


class AddDonation(View):
    def get(self, request):
        return render(request, "form.html")


class Login(View):
    def get(self, request):
        return render(request, "login.html")


class Register(View):
    def get(self, request):
        form = RegisterForm(auto_id=False)
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            # form.cleaned_data.pop
            user = User.objects.create(
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
                username=form.cleaned_data["email"]
            )
            return redirect("login")
        return render(request, "register.html", {"form": form})
