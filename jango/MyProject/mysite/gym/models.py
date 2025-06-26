from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Subscription(models.Model):
    avail_participations = models.IntegerField()
    def __str__(self):
        return f"Subscription {self.pk} – avail: {self.avail_participations}"

class Payment(models.Model):
    tran_id      = models.AutoField(primary_key=True)
    user         = models.ForeignKey(
                       settings.AUTH_USER_MODEL,
                       on_delete=models.CASCADE,
                       related_name="payments"
                   )
    subscription = models.ForeignKey(
                       Subscription,
                       on_delete=models.CASCADE,
                       db_column="sub_id",         # αν θες να κρατήσεις το ίδιο όνομα στη βάση
                       related_name="payments"
                   )
    amount       = models.DecimalField(max_digits=10, decimal_places=2)
    tran_date    = models.DateTimeField()

    def __str__(self):
        return f"Payment {self.tran_id} – €{self.amount}"


#
# 3) Member
#
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
    # Στο διάγραμμα, Member έχει ένα FK προς Subscription (sub_id)
    sub = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="sub_id",
        related_name="members"
    )
    # Και ένα FK προς Payment (tran_id)
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


#
# 4) Employee  (για να είναι superclass του Secretary/Coach)
#
class Employee(models.Model):
    em_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    age = models.IntegerField()
    phone_num = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} {self.surname}"


#
# 5) Secretary κληρονομεί από Employee
#
class Secretary(Employee):
    # Αν δεν χρειάζεται επιπλέον πεδία, απλώς pass
    class Meta:
        verbose_name = "Secretary"
        verbose_name_plural = "Secretaries"


#
# 6) Coach κληρονομεί από Employee
#
class Coach(Employee):
    # Αν δεν χρειάζεται επιπλέον πεδία, απλώς pass
    class Meta:
        verbose_name = "Coach"
        verbose_name_plural = "Coaches"


#
# 7) Class  (ιδιαίτερη προσοχή: ο Coach είναι FK εδώ)
#
class Class(models.Model):
    cl_id = models.AutoField(primary_key=True)
    # Κάθε μάθημα (Class) συνδέεται με έναν Coach (FK)
    em = models.ForeignKey(
        Coach,
        on_delete=models.CASCADE,
        db_column="em_id",
        related_name="classes"
    )
    dates = models.DateTimeField()        # ή DateField, ανάλογα με το πόσο ακριβές θέλεις
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.dates.date()})"


#
# 8) History
#
class History(models.Model):
    h_id = models.AutoField(primary_key=True)
    # FK προς Member
    user = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="histories"
    )
    # FK προς Class
    cl = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        db_column="cl_id",
        related_name="histories"
    )
    date = models.DateTimeField()

    def __str__(self):
        return f"History {self.h_id}: Member {self.user.username} - Class {self.cl.name}"
