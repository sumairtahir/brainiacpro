from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view, name="user_profile"),
    path('/change-password', views.change_password_view, name="change_password"),
    path('/billing', views.billing_view, name="billing"),
]