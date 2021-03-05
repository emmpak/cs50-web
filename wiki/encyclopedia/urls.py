from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("random/", views.random, name="random"),
    path("<str:title>/edit/", views.edit, name="edit")
]


# path("entries/"), # GET and POST; index can redirect to this
# path("entries?title=") # search
