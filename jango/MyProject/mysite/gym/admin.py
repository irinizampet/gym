from django.contrib import admin

# Register your models here.
# gym/admin.py

from django.contrib import admin
from .models import (
    Subscription,
    Payment,
    Member,
    Employee,
    Secretary,
    Coach,
    Class,
    History,
    Booking,
    Cancellation
)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('sub_id', 'avail_participations')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('tran_id', 'sub', 'amount', 'tran_date')
    list_filter = ('tran_date',)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email', 'sub', 'tran', 'registration_date')
    search_fields = ('username', 'email', 'name', 'surname')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('em_id', 'name', 'surname', 'email', 'phone_num')

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('em_id', 'name', 'surname', 'email')

@admin.register(Secretary)
class SecretaryAdmin(admin.ModelAdmin):
    list_display = ('em_id', 'name', 'surname', 'email')

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('cl_id', 'name', 'dates', 'capacity', 'em')

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('h_id', 'user', 'cl', 'date')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('h_id', 'em_id', 'name', 'surname')

@admin.register(Cancellation)
class CancellationAdmin(admin.ModelAdmin):
    list_display = ('h_id', 'em_id', 'name', 'surname')
