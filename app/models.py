from django.db import models
from django.contrib.auth.models import User

TYPE = (
    (1, "Fundacja"),
    (2, "Organizacja pozarządowa"),
    (3, "Zbiórka lokalna")
)


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    type = models.IntegerField(choices=TYPE)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=30)
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=20)
    pick_up_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    pick_up_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)