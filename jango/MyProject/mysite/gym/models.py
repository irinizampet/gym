from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models import Q, CheckConstraint, UniqueConstraint
from django.core.exceptions import ValidationError


class Subscription(models.Model):
    sub_id               = models.AutoField(primary_key=True)
    name                 = models.CharField(max_length=50)
    avail_participations = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.avail_participations})"


class Payment(models.Model):
    """
    Καταγράφει την πληρωμή ενός πακέτου από χρήστη.
    """
    tran_id       = models.AutoField(primary_key=True)
    user          = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    user        = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
        null=True,
        blank=True,
    )
    subscription  = models.ForeignKey(
        Subscription,
        on_delete=models.PROTECT,
        related_name="payments",
        null=True,
        blank=True,
    )
    amount        = models.DecimalField(max_digits=8, decimal_places=2)
    tran_date     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.tran_id} by {self.user}"


#
# 3) Member
#
#class Member(models.Model):
 #   user_id = models.AutoField(primary_key=True)
  # surname = models.CharField(max_length=30)
   # registration_date = models.DateTimeField(auto_now_add=True)
    #phone_num = models.CharField(max_length=15,default="")
    #email = models.EmailField(unique=True)
    #username = models.CharField(max_length=20, unique=True)
   # password = models.CharField(max_length=128)
    # Στο διάγραμμα, Member έχει ένα FK προς Subscription (sub_id)
    #sub = models.ForeignKey(
     #   Subscription,
      #  on_delete=models.SET_NULL,
       # null=True,
        #blank=True,
      #  db_column="sub_id",
       # related_name="members"
    #)
    # Και ένα FK προς Payment (tran_id)
   # tran = models.ForeignKey(
    #    Payment,
     #   on_delete=models.SET_NULL,
      #  null=True,
       # blank=True,
        #db_column="tran_id",
       # related_name="members"
    #)

    #def __str__(self):
     #   return self.username

     # gym/models.py

class Member(AbstractUser):
    """
    Custom user: κληρονομεί όλα τα πεδία του AbstractUser
    (username, password, email, first_name, last_name, is_staff, is_active, κλπ)
    και προσθέτει:
      - registration_date
      - phone_num
    """
    registration_date = models.DateTimeField(auto_now_add=True)
    phone_num         = models.CharField(max_length=15, blank=True)

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
    """
    Ένα τμήμα/μάθημα στο γυμναστήριο.
    """
    cl_id      = models.AutoField(primary_key=True)
    em = models.ForeignKey(
        Coach,
        on_delete=models.CASCADE,
        db_column="em_id",
        related_name="classes",
    )
    name       = models.CharField(max_length=100)
    date_time  = models.DateTimeField()
    capacity   = models.PositiveIntegerField()
    description= models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} @ {self.date_time:%Y-%m-%d %H:%M}"

    @property
    def booked_count(self):
        return self.history.filter(cl__isnull=False).count()

    def is_full(self):
        return self.booked_count >= self.capacity

#
# 8) History  (γενικός πίνακας, “γονέας” για Booking & Cancellation)
#
class History(models.Model):
    """
    Ενιαίο log για:
      - αγορές πακέτων (sub != None, cl = None)
      - κρατήσεις μαθημάτων (sub = None, cl != None)
    """
    h_id   = models.AutoField(primary_key=True)
    user   = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="history"
    )
    sub    = models.ForeignKey(
        Subscription, null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="+"
    )
    cl     = models.ForeignKey(
        Class, null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="history"
    )
    date   = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # είτε purchase είτε booking, όχι και τα δύο
            models.CheckConstraint(
                check=(
                    (Q(sub__isnull=False) & Q(cl__isnull=True)) |
                    (Q(sub__isnull=True) & Q(cl__isnull=False))
                ),
                name="history_either_sub_or_cl"
            ),
            # αποτρέπουμε διπλο-κράτηση στο ίδιο μάθημα
            models.UniqueConstraint(
                fields=["user", "cl"],
                condition=Q(cl__isnull=False),
                name="unique_user_class_booking"
            ),
        ]

    def clean(self):
        # επιπλέον validation
        if bool(self.sub) == bool(self.cl):
            raise ValidationError("Ιστορικό πρέπει να είναι είτε purchase είτε booking.")

    def is_purchase(self):
        return self.sub is not None

    def is_booking(self):
        return self.cl is not None

    def __str__(self):
        if self.sub:
            return f"[Purchase] {self.user} -> {self.sub}"
        else:
            return f"[Booking] {self.user} -> {self.cl}"
