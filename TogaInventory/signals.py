from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Deposit

@receiver(post_save, sender=Deposit)
def handle_deposit_post_save(sender, instance, created, **kwargs):
    """
    Triggers summary refresh after a deposit is created or updated.
    """
    instance.inventory.update_deposit_summary()

@receiver(post_delete, sender=Deposit)
def handle_deposit_post_delete(sender, instance, **kwargs):
    """
    Ensures financial accuracy if a deposit record is purged from the database.
    """
    if instance.inventory:
        instance.inventory.update_deposit_summary()