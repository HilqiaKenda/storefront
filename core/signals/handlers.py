from django.dispatch import receiver
from store.signals import order_created as Baseorder_created

@receiver(Baseorder_created)
def order_created(sender, **kwargs):
    print(kwargs['order'])