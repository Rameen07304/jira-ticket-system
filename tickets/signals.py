from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import tickets

@receiver(pre_save, sender=tickets)
def store_old_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_ticket = tickets.objects.get(pk=instance.pk)
            instance._old_status = old_ticket.status
        except tickets.DoesNotExist:
            instance._old_status = None
@receiver(post_save, sender=tickets)
def ticket_post_save_handler(sender, instance, created, **kwargs):
    if created:
        print(f"[Signal] New ticket created for user: {instance.user.username}, Subject: {instance.subject}")
    else:
        old_status = getattr(instance, '_old_status', None)
        if old_status and old_status != instance.status:
            print(f" Ticket status changed for user: {instance.user.username}")
            print(f" Subject: {instance.subject}")
            print(f" Old Status: {old_status} -> New Status: {instance.status}")
