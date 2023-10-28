from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('get-started/', views.get_started, name='get_started'),
    path("activate-account/<str:uidb64>/<str:token>", views.activate , name="activate_account"),
    path("forgot-password", views.forgotPassword , name="forgot_password"),
    path("reset-password-validate/<str:uidb64>/<str:token>", views.resetpassword_validate , name="resetpassword_validate"),
    path("reset-password", views.resetPassword , name="reset_passowrd"),
]