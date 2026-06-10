from django.apps import AppConfig


class TogainventoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "TogaInventory"
    
    # Customizing the structural string label rendered inside admin dashboard views
    verbose_name = "Order Accounting & Ledgers"

    def ready(self):
        """
        Application operational initialization wrapper block.
        Safely registers the signals matrix to prevent recursive importing issues.
        """
        import TogaInventory.signals