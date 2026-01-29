from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db.models import Q
from datetime import date  

from .models import UserProfile, Pet, Match, Message, PET_TYPES

class PetSerializer(serializers.ModelSerializer):
    weight = serializers.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        allow_null=True, 
        required=False,
        validators=[MinValueValidator(0.01, message="Waga musi być dodatnia.")]
    )
    
    age = serializers.IntegerField(
        validators=[
            MinValueValidator(0, message="Wiek nie może być ujemny."),
            MaxValueValidator(100, message="Wiek jest nierealistycznie wysoki.")
        ]
    )

    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'pet_type', 'breed', 'weight', 
            'description', 'is_friendly', 'age'
        ]
        read_only_fields = ['id']

    def validate_name(self, value):
        if not value[0].isupper():
            raise serializers.ValidationError(
                "Imię pupila powinno rozpoczynać się wielką literą!"
            )
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    
    first_name = serializers.CharField(
        max_length=50,
        validators=[MaxLengthValidator(50)]
    )

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        
        birth_date = data.get('birth_date')
        
        if birth_date and (date.today().year - birth_date.year) < 18:
            raise serializers.ValidationError(
                {"birth_date": "Aby korzystać z aplikacji, musisz mieć ukończone 18 lat."}
            )
            
        first_name = data.get('first_name')
        if first_name and not first_name[0].isupper():
             raise serializers.ValidationError(
                {"first_name": "Imię powinno rozpoczynać się wielką literą!"}
            )

        return data


class MatchSerializer(serializers.ModelSerializer):
    
    swiper_name = serializers.CharField(source='swiper.first_name', read_only=True)
    target_name = serializers.CharField(source='target.first_name', read_only=True)

    class Meta:
        model = Match
        fields = ['id', 'swiper', 'target', 'is_match', 'timestamp', 'swiper_name', 'target_name']
        read_only_fields = ['id', 'is_match', 'timestamp', 'swiper_name', 'target_name']
        
        validators = [
            UniqueTogetherValidator(
                queryset=Match.objects.all(),
                fields=['swiper', 'target'],
                message="To polubienie już istnieje. Nie możesz polubić tej osoby dwukrotnie."
            )
        ]

    def validate(self, data):
        if data['swiper'] == data['target']:
            raise serializers.ValidationError("Nie możesz polubić własnego profilu.")
        return data


class MessageSerializer(serializers.ModelSerializer):
    
    sender_name = serializers.CharField(source='sender.first_name', read_only=True)
    recipient_name = serializers.CharField(source='recipient.first_name', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'match', 'sender', 'recipient', 'content', 'timestamp', 'sender_name', 'recipient_name']
        read_only_fields = ['id', 'timestamp', 'sender_name', 'recipient_name']
        
    def validate(self, data):
        
        match_instance = data.get('match')
        sender = data.get('sender')
        recipient = data.get('recipient')
        
        is_participant = (sender == match_instance.swiper and recipient == match_instance.target) or \
                         (sender == match_instance.target and recipient == match_instance.swiper)
        
        if not is_participant:
            raise serializers.ValidationError(
                "Nadawca i odbiorca muszą być stronami powiązanymi z tym dopasowaniem."
            )
            
        if not match_instance.is_match:
            raise serializers.ValidationError(
                "Nie można wysłać wiadomości: Dopasowanie nie jest wzajemne."
            )

        return data


