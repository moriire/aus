from django.db import models
from agent.models import Agent

class House(models.Model):
    class GOAL(models.TextChoices):
        RENT = "rent"
        SALE = "sale"
        SHORTLET = "shortlet"
    class Model(models.TextChoices):
        bungalow = "BUNGALOW"
        duplex = "DUPLEX"
        selfcontain = "SELFCONTAIN"
    agent = models.ForeignKey(Agent, related_name="house_agent", on_delete=models.CASCADE)
    location = models.CharField(max_length=25)
    desc = models.TextField(max_length=300)
    address = models.TextField(max_length=150)
    model = models.CharField(max_length=30, choices=Model.choices)
    goal = models.CharField(max_length=10, choices=GOAL.choices)

    def __str__(self) -> str:
        return self.model
