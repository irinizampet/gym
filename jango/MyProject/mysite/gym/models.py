from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Subscription(models.Model):
    sub_id = models.AutoField(primary_key=True)
    avail_participations = models.IntegerField()

    def __str__(self):
        return f"Subscription {self.sub_id} - avail: {self.avail_participations}"


class Payment(models.Model):
    tran_id = models.AutoField(primary_key=True)
    sub = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        db_column="sub_id",     
        related_name="payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tran_date = models.DateTimeField()

    def __str__(self):
        return f"Payment {self.tran_id} - €{self.amount}"



class Member(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    age = models.IntegerField(null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    phone_num = models.CharField(max_length=15,default="")
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    
    sub = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="sub_id",
        related_name="members"
    )
    
    tran = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="tran_id",
        related_name="members"
    )

    def __str__(self):
        return self.username



class Employee(models.Model):
    em_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    age = models.IntegerField()
    phone_num = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} {self.surname}"



class Secretary(Employee):

    class Meta:
        verbose_name = "Secretary"
        verbose_name_plural = "Secretaries"



class Coach(Employee):
    
    class Meta:
        verbose_name = "Coach"
        verbose_name_plural = "Coaches"



class Class(models.Model):
    cl_id = models.AutoField(primary_key=True)
    
    em = models.ForeignKey(
        Coach,
        on_delete=models.CASCADE,
        db_column="em_id",
        related_name="classes"
    )
    dates = models.DateTimeField()       
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.dates.date()})"



class History(models.Model):
    h_id = models.AutoField(primary_key=True)
    
    user = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="histories"
    )
    
    cl = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        db_column="cl_id",
        related_name="histories"
    )
    date = models.DateTimeField()

    def __str__(self):
        return f"History {self.h_id}: Member {self.user.username} - Class {self.cl.name}"






