from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class User(AbstractUser):
    def __str__(self):
        return self.last_name


class Client(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True, null=False)
    mobile = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=250, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="clients"
    )

    def __str__(self):
        return f"Client : {self.last_name} - working for {self.company_name}"


class Contract(models.Model):
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="contracts",
    )
    client = models.ForeignKey(
        to=Client, on_delete=models.CASCADE, related_name="contracts"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False, verbose_name="signed")
    amount = models.FloatField()
    payment_due = models.DateField(auto_now=True)

    def __str__(self):
        return f"Contract attached to {self.client} - Status : {self.status} - Amount : {self.amount} - Payment due {self.payment_due}"


class Event(models.Model):
    STATUS_CHOICES = [("IN_PROGRESS", "In progress"), ("DONE", "done")]

    client = models.ForeignKey(
        to=Client, on_delete=models.CASCADE, related_name="events"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="events"
    )
    event_status = models.CharField(choices=STATUS_CHOICES, max_length=20)
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    note = models.TextField()

    def __str__(self):
        return f"Event attached to {self.client} - Status : {self.event_status} - Attendees : {self.attendees} - Event date {self.event_date}"
