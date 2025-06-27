from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('περιβαλλον/', views.dashboard_view, name='περιβαλλονχρηστη'),
    path('signup/', views.signup_view, name='signup'),
    path('passreset/', views.password_reset_view, name='passreset'),
    path('', views.index_view, name='index'),
    path('filosofia/', views.filosofia_view, name='filosofia'),
    path('prop/', views.προπονητες_view, name='Προπονητές'),
    path('contact/', views.contact_view, name='contact'),
    path('programmaaaa/', views.Programmata_view, name='Πρόγραμμα'),
    path('payment/', views.payment_view, name='payment'),
    path('profil/', views.profil_view, name='profil'),
    path('booking/', views.booking_view, name='booking'),
    path('history/', views.history_view, name='training-history'),
    path('announcement/', views.announcements_view, name='announcement'),

]


