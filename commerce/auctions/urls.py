from django.urls import path

from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("login", views.login_view, name="login"),
  path("logout", views.logout_view, name="logout"),
  path("register", views.register, name="register"),
  path("add", views.add, name="add"),
  path("categories", views.categories, name="categories"),
  path("categories/<str:category>", views.category, name="category"),
  path("listings/<str:listing_id>", views.listing_page, name="listing_page")
]
