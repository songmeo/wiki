from django.urls import path
from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("random", views.random, name="random"),
    path("search/", views.search, name="search"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("<str:title>", views.entry, name="entry"),
]
