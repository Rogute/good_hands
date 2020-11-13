from django.shortcuts import render
from django.views import View
from .models import Donation
from django.db.models import Sum


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
        return render(request, "register.html")
