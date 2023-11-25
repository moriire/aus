from django.db import models
from user.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Agent(models.Model):
    user = models.OneToOneField(User, related_name="agent_user", on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    location = models.CharField(max_length=25)
    def __str__(self) -> str:
        return self.phone
    

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Agent.objects.create(user=instance)
        instance.agent_user.save()