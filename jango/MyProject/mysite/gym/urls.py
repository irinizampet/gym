from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('περιβαλλον/', views.dashboard_view, name='περιβαλλονχρηστη'),
]
