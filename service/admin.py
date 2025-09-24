# service/admin.py
from django.contrib import admin
from .models import Client, Provider, Reservation

# Enregistrez vos modèles ici
admin.site.register(Client)
admin.site.register(Provider)
admin.site.register(Reservation)