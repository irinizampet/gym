from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('περιβαλλον/', views.dashboard_view, name='περιβαλλονχρηστη'),
    path('signup/', views.signup_view, name='signup'),
    path('passreset/', views.password_reset_view, name='passreset'),


]

