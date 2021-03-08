from django.shortcuts import render, redirect
from django.views import View
from .models import Donation, Category, Institution
from django.contrib.auth.models import User
from django.db.models import Sum
from .forms import RegisterForm, LoginForm, EditProfileForm
from django.contrib.auth import authenticate, login, logout


class LandingPageView(View):
    def get(self, request):
        # quantity from Donation
        sum_of_bags = Donation.objects.aggregate(value=Sum('quantity'))
        institution_supported = Donation.objects.aggregate(value=Sum('institution'))
        foundations = Institution.objects.filter(type=1)
        non_governmental_organizations = Institution.objects.filter(type=2)
        local_collection = Institution.objects.filter(type=3)
        ctx = {
            "sum_of_bags": sum_of_bags,
            "institution_supported": institution_supported,
            "foundations": foundations,
            "non_governmental_organizations": non_governmental_organizations,
            "local_collection": local_collection
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

    def post(self, request):
        categories = request.POST.get('categories')
        quantity = request.POST.get('bags')
        institution = Institution.objects.get(pk=request.POST.get('institutions'))
        address = request.POST.get('address')
        phone_number = request.POST.get('phone')
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        pick_up_date = request.POST.get('data')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')
        user = User.objects.get(pk=request.user.id)
        new_donation = Donation.objects.create(
            quantity=quantity,
            institution=institution,
            address=address,
            phone_number=phone_number,
            city=city,
            zip_code=zip_code,
            pick_up_date=pick_up_date,
            pick_up_time=pick_up_time,
            pick_up_comment=pick_up_comment,
            user=user,
        )
        new_donation.categories.add(*request.POST.getlist("categories"))

        return render(request, 'form-confirmation.html')


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
            donations = Donation.objects.filter(is_taken=False, user_id=user.id)
            donations_taken = Donation.objects.filter(is_taken=True, user_id=user.id)
            ctx = {
                'user': user,
                'donations': donations,
                'donations_taken': donations_taken
            }
            return render(request, 'user_profile.html', ctx)


class EditProfileView(View):
    def get(self, request):
        form = EditProfileForm()
        return render(request, 'user_update.html', {"form": form})

    def post(self, request):
        user = request.user
        form = EditProfileForm(request.POST, isinstance=user)
        if form.is_valid():
            form.save()
            return redirect('profil')

