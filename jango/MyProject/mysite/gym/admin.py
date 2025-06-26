from django.contrib import admin
from .models import (
    Subscription,
    Payment,
    Member,
    Employee,
    Secretary,
    Coach,
    Class as GymClass,
    History,
)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "avail_participations")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("tran_id", "user", "subscription", "amount", "tran_date")
    list_filter  = ("subscription",)
    search_fields = ("tran_id",)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "username",
        "email",
        "name",
        "surname",
        "age",
        "registration_date",
        "phone_num",
        "sub",
        "tran",
    )
    list_filter  = ("sub", "tran", "age")
    search_fields = ("username", "email", "name", "surname")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display   = ("em_id", "name", "surname", "age", "phone_num", "email")
    search_fields  = ("name", "surname", "email")


@admin.register(Secretary)
class SecretaryAdmin(EmployeeAdmin):
    """κληρονομεί όλη την εμφάνιση από EmployeeAdmin"""


@admin.register(Coach)
class CoachAdmin(EmployeeAdmin):
    """κληρονομεί όλη την εμφάνιση από EmployeeAdmin"""


@admin.register(GymClass)
class ClassAdmin(admin.ModelAdmin):
    list_display   = ("cl_id", "name", "dates", "em", "capacity")
    list_filter    = ("em", "dates")
    search_fields  = ("name", "description")


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ("h_id", "user", "cl", "date")
    list_filter  = ("user", "cl", "date")
