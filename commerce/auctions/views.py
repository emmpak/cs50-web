from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, DecimalField

from .models import User, Listing

class ListingForm(ModelForm):
  class Meta:
    model = Listing
    fields = ['title', 'description', 'category', 'image_url', 'cents', 'currency']
    field_classes = { 'cents': DecimalField }
    labels = { 'cents': 'Price' }


def index(request):
  return render(request, "auctions/index.html", {
    "listings": Listing.objects.all()
  })

def add(request):
  if request.method == "POST":
    form = ListingForm(request.POST)
    if form.is_valid():
      listing = form.save(commit=False)
      listing.cents = int(form.cleaned_data['cents'] * 100)
      listing.user = request.user
      listing.save()
      return HttpResponseRedirect(reverse('add'))
  else:
    return render(request, "auctions/add_listing.html", {
      "form": ListingForm()
    })

def categories(request):
  return render(request, "auctions/categories.html", {
    "categories": Listing.objects.values_list("category", flat=True).distinct().order_by("category")
  })

def login_view(request):
  if request.method == "POST":

    # Attempt to sign user in
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    # Check if authentication successful
    if user is not None:
      login(request, user)
      return HttpResponseRedirect(reverse("index"))
    else:
      return render(request, "auctions/login.html", {
        "message": "Invalid username and/or password."
      })
  else:
    return render(request, "auctions/login.html")


def logout_view(request):
  logout(request)
  return HttpResponseRedirect(reverse("index"))


def register(request):
  if request.method == "POST":
    username = request.POST["username"]
    email = request.POST["email"]

    # Ensure password matches confirmation
    password = request.POST["password"]
    confirmation = request.POST["confirmation"]
    if password != confirmation:
      return render(request, "auctions/register.html", {
        "message": "Passwords must match."
      })

    # Attempt to create new user
    try:
      user = User.objects.create_user(username, email, password)
      user.save()
    except IntegrityError:
      return render(request, "auctions/register.html", {
        "message": "Username already taken."
      })
    login(request, user)
    return HttpResponseRedirect(reverse("index"))
  else:
    return render(request, "auctions/register.html")
