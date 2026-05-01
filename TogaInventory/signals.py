from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Deposit

@receiver(post_save, sender=Deposit)
def update_inventory_after_deposit(sender, instance, created, **kwargs):
    if created:
        instance.inventory.update_deposit_summary()
