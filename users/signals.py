from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, ProfileLog, Plan


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        #not safe
        profile = Profile.objects.create(user=instance, code=Profile.generateCode())





@receiver(pre_save, sender=Profile)
def save_profile(sender, instance, **kwargs):
    if instance.id is not None:
        prev = Profile.objects.get(pk=instance.id)
        log = ProfileLog.objects.create(profile=instance, prev_balance=prev.balance, prev_plan=prev.plan.name, new_plan=instance.plan.name, new_balance=instance.balance)
        log.save()