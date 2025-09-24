from rest_framework import generics, views, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.middleware.csrf import get_token
from .models import Client, Provider, Reservation
from django.shortcuts import render
from .serializers import (
    ClientSerializer, ProviderSerializer,
    ReservationSerializer, LoginSerializer
)

# Vue pour le rendu du template principal de l'application React
def index_view(request):
    context = {}
    return render(request, 'service/appli.html', context)

# --- Vues pour les Clients ---

class ClientListCreate(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = [permissions.AllowAny]  # Permet l'accès à tous pour la création

    def get_queryset(self):
        return Client.objects.all()  # Retourne tous les clients

    def perform_create(self, serializer):
        name = serializer.validated_data.get('name')
        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number') # Get phone number
        username = self.request.data.get('username', email)
        password = self.request.data.get('password')

        if not password:
            raise ValidationError({"password": "Le mot de passe est requis pour la création d'un nouvel utilisateur."})

        try:
            with transaction.atomic():
                user = User.objects.create_user(username=username, email=email, password=password)
                serializer.save(user=user, phone_number=phone_number) # Save phone number
        except Exception as e:
            raise ValidationError({"detail": f"Erreur lors de la création de l'utilisateur ou du client: {e}"})


class ClientRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]  # Accès uniquement pour les utilisateurs authentifiés

    def get_queryset(self):
        user = self.request.user
        # For admin, they can access any client. For clients, they can only access their own.
        if user.is_superuser:
            return Client.objects.all()
        elif hasattr(user, 'client_profile'):
            return Client.objects.filter(user=user)
        return Client.objects.none()

    def perform_update(self, serializer):
        # Update specific fields if they are in the request data
        if 'phone_number' in self.request.data:
            serializer.save(phone_number=self.request.data['phone_number'])
        else:
            serializer.save()  # Met à jour le profil du client

    def perform_destroy(self, instance):
        user = instance.user
        instance.delete()
        user.delete()  # Supprime l'utilisateur Django associé

# --- Vues pour les Prestataires ---

class ProviderListCreate(generics.ListCreateAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = [permissions.AllowAny]  # Permet l'accès à tous pour la création

    def perform_create(self, serializer):
        name = serializer.validated_data.get('name')
        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number') # Get phone number
        username = self.request.data.get('username', email)
        password = self.request.data.get('password')

        if not password:
            raise ValidationError({"password": "Le mot de passe est requis pour la création d'un nouvel utilisateur."})

        try:
            with transaction.atomic():
                user = User.objects.create_user(username=username, email=email, password=password)
                serializer.save(user=user, phone_number=phone_number) # Save phone number
        except Exception as e:
            raise ValidationError({"detail": f"Erreur lors de la création de l'utilisateur ou du prestataire: {e}"})


class ProviderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = [permissions.IsAuthenticated]  # Accès uniquement pour les utilisateurs authentifiés

    def get_queryset(self):
        user = self.request.user
        # For admin, they can access any provider. For providers, they can only access their own.
        if user.is_superuser:
            return Provider.objects.all()
        elif hasattr(user, 'provider_profile'):
            return Provider.objects.filter(user=user)
        return Provider.objects.none()

    def perform_update(self, serializer):
        # Update specific fields if they are in the request data
        if 'phone_number' in self.request.data:
            serializer.save(phone_number=self.request.data['phone_number'])
        else:
            serializer.save() # Met à jour le profil du prestataire

    def perform_destroy(self, instance):
        user = instance.user
        instance.delete()
        user.delete()  # Supprime l'utilisateur Django associé

# --- Vues pour les Réservations ---

class ReservationListCreate(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Reservation.objects.all()
        elif hasattr(user, 'client_profile'):
            return Reservation.objects.filter(client=user.client_profile)
        elif hasattr(user, 'provider_profile'):
            return Reservation.objects.filter(provider=user.provider_profile)
        return Reservation.objects.none()

    def perform_create(self, serializer):
        serializer.save()  # Crée la réservation sans restrictions

class ReservationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]  # Accès uniquement pour les utilisateurs authentifiés

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Reservation.objects.all()  # L'administrateur voit toutes les réservations
        elif hasattr(user, 'client_profile'):
            return Reservation.objects.filter(client=user.client_profile)  # Un client voit uniquement ses propres réservations
        elif hasattr(user, 'provider_profile'):
            return Reservation.objects.filter(provider=user.provider_profile)  # Un prestataire voit uniquement ses réservations
        return Reservation.objects.none()  # Aucun autre type d'utilisateur ne voit de réservations

# --- Vues d'Authentification ---

class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        login(request, user)
        csrf_token = get_token(request)

        user_type = 'user'  # Type par défaut
        profile_id = user.id  # ID de l'utilisateur par défaut
        profile_phone_number = None # Initialize phone number

        if user.is_superuser:
            user_type = 'admin'
        elif hasattr(user, 'client_profile'):
            user_type = 'client'
            profile_id = user.client_profile.id
            profile_phone_number = user.client_profile.phone_number # Get client phone number
        elif hasattr(user, 'provider_profile'):
            user_type = 'provider'
            profile_id = user.provider_profile.id
            profile_phone_number = user.provider_profile.phone_number # Get provider phone number

        response = Response({
            'message': 'Connexion réussie',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'user_type': user_type,
                'profile_id': profile_id,
                'phone_number': profile_phone_number # Return phone number on login
            }
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            'csrftoken',
            csrf_token,
            httponly=False,
            samesite='Lax',
            secure=False  # Mettre à True en production avec HTTPS
        )

        return response

class LogoutView(views.APIView):
    permission_classes = [permissions.AllowAny]  # Permet l'accès à tous

    def post(self, request):
        logout(request)
        response = Response({"message": "Déconnexion réussie"}, status=status.HTTP_200_OK)
        response.delete_cookie('sessionid')
        response.delete_cookie('csrftoken')
        return response
