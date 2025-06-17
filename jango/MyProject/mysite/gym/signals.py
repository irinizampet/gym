from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment, History

@receiver(post_save, sender=Payment)
def log_payment(sender, instance, created, **kwargs):
    if created:
        History.objects.create(
          user=instance.user,
          sub=instance.subscription
        )
