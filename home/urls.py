from django.urls import path
from . import views
from django.views.decorators.cache import cache_page


app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]