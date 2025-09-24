from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True) 
    def __str__(self):
        return self.name

class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    name = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True) 
    
    def __str__(self):
        return f"{self.name} ({self.service})"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuvée'),
        ('rejected', 'Rejetée'),
        ('completed', 'Terminée'),
        ('cancelled', 'Annulée'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reservations')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='reservations')
    service = models.CharField(max_length=200)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Réservation #{self.id} - {self.client.name} avec {self.provider.name}"
