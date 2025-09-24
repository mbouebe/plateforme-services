from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Client, Provider, Reservation

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'email', 'phone_number'] # Added phone_number

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['id', 'name', 'service', 'email', 'phone_number'] # Added phone_number

class ReservationSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    # Add phone numbers for related client/provider in reservations for easy access
    client_phone_number = serializers.CharField(source='client.phone_number', read_only=True)
    provider_phone_number = serializers.CharField(source='provider.phone_number', read_only=True)
    
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )
        
        if not user:
            raise serializers.ValidationError("Identifiants invalides")
        
        if data['role'] == 'admin' and not user.is_superuser:
            raise serializers.ValidationError("Accès administrateur refusé")
        
        if data['role'] == 'client' and not hasattr(user, 'client_profile'):
            raise serializers.ValidationError("Profil client non trouvé")
        
        if data['role'] == 'provider' and not hasattr(user, 'provider_profile'):
            raise serializers.ValidationError("Profil prestataire non trouvé")
        
        data['user'] = user
        return data
