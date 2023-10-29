from rest_framework.authtoken.views import obtain_auth_token # this will give us token if we send username and password

from django.urls import path

from . import views

urlpatterns = [
    path("login/", obtain_auth_token, name="login"),
    path("register/", views.registration_view, name="register"),
    path("logout/", views.Logout_View, name="logout"),
]