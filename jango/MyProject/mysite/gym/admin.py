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
)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('sub_id', 'name', 'avail_participations')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('tran_id', 'user', 'subscription', 'amount', 'tran_date')
    list_filter  = ('subscription', 'tran_date')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display   = (
        'id', 'username', 'email',
        'first_name', 'last_name',
        'registration_date', 'phone_num'
    )
    search_fields  = ('username', 'email', 'first_name', 'last_name')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('em_id', 'name', 'surname', 'email', 'phone_num')

@admin.register(Secretary)
class SecretaryAdmin(admin.ModelAdmin):
    # Secretary κληρονομεί απευθείας τα πεδία του Employee
    list_display = ('em_id', 'name', 'surname', 'email', 'phone_num')

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    # Coach κληρονομεί απευθείας τα πεδία του Employee
    list_display = ('em_id', 'name', 'surname', 'email', 'phone_num')

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    # το πεδίο στο model λέγεται `em` και `date_time`
    list_display = ('cl_id', 'em', 'name', 'date_time', 'capacity')
    list_filter  = ('em',)

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('h_id', 'user', 'sub', 'cl', 'date')
    list_filter  = ('sub', 'cl', 'date')
