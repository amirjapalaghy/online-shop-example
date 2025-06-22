from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('login', views.UserLoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('check_otp', views.CheckOtpView.as_view(), name='check_otp'),
    path('logout', views.logout_user, name='logout'),
]