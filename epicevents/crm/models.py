from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class User(AbstractUser):
    ROLE = [("MANAGEMENT", "management"), ("SALES", "sales"), ("SUPPORT", "support")]

    role = models.CharField(choices=ROLE, max_length=20)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(unique=True, max_length=30)
    password = models.CharField()

    def __str__(self):
        return f"{self.pk} - {self.last_name} - {self.first_name} - {self.username}"


class Client(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    phone = models.CharField(unique=True)
    mobile = models.CharField(unique=True)
    company_name = models.CharField(max_length=250)
    client_status = models.BooleanField(default=False, verbose_name="Under contract")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="clients"
    )

    def __str__(self):
        return f"Client {self.pk} : {self.last_name} - Company : {self.company_name}"


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
    status = models.BooleanField(default=False, verbose_name="Signed")
    amount = models.FloatField()
    payment_due = models.DateField()

    def __str__(self):
        return f"Contract {self.pk} - {self.client} - Status : {self.status} - Amount : {self.amount} - Payment due {self.payment_due}"


class Event(models.Model):
    STATUS_CHOICES = [("COMING", "Coming"), ("DONE", "done")]

    client = models.ForeignKey(
        to=Client, on_delete=models.CASCADE, related_name="events"
    )
    contract = models.ForeignKey(
        to=Contract, on_delete=models.CASCADE, related_name="events"
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
        return f"Event {self.pk} attached to {self.client} - Status : {self.event_status} - Attendees : {self.attendees} - Event date {self.event_date}"
