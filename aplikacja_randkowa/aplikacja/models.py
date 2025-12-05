from django.db import models
from django.db.models import UniqueConstraint, Q
from datetime import date




# Lista pupili
PET_TYPES = (
    ('', '--- Nic / Nie Wybrano ---'),
    ('P', 'Pies'),
    ('K', 'Kot'),
    ('G', 'Gryzoń'),
    ('B', 'Ptak'),
    ('R', 'Ryba'),
    ('H', 'Koń'),
    ('J', 'Jaszczur'),
    ('I', 'Inne'),
)


# Wybór płci 
GENDER_CHOICES = models.IntegerChoices(
    'Płeć',
    'Kobieta Mężczyzna Inna Nie podano'
)


#Jaki jest pupil
class Pet(models.Model):
    name = models.CharField(max_length=50, help_text="Imię zwierzaka.", verbose_name="Imie pupila")
    pet_type = models.CharField(
        max_length=1, 
        choices=PET_TYPES, 
        default='',
        help_text="Typ zwierzaka, np. Pies, Kot."
    )
    breed = models.CharField(max_length=100, blank=True, help_text="Rasa pupila (jeśli dotyczy).")
    weight = models.DecimalField(
        max_digits = 5,
        decimal_places = 2,
        null = True,
        help_text="Waga pupila w kg"
    )
    description = models.TextField(blank=True, help_text="Krótki opis charakteru pupila.")
    is_friendly = models.BooleanField(
        default=True, 
        help_text="Czy pupil jest przyjazny i lubi towarzystwo?"
    )
    # Wiek zwierzaka 
    age = models.PositiveSmallIntegerField(
        default=1,
        help_text="Wiek pupila w latach."
    )

    def __str__(self):
        return f"{self.name} ({self.get_pet_type_display()})"
    
    class Meta:
         verbose_name="Pupil"
         verbose_name_plural = "Pupile"
         ordering = ['name'] 


#Profil uzytkownika
class UserProfile(models.Model):
    email = models.EmailField(unique=True, help_text="Adres email (login)")
    password = models.CharField(max_lenght = 128, editable=False)
    avatar = models.ImageField(
         upload_to='avatars',
         blank=True,
         null=True,
         help_text="Zdjecie profilowe"
    )

    birth_date = models.DateField(
         null=True,
         blank=True,
         help_text="Data urodzenia"
    )
    first_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50, help_text="Miasto, w którym mieszkacie (Ty i Twój pupil).")
    gender = models.IntegerField(
        choices=GENDER_CHOICES.choices, 
        default=GENDER_CHOICES.Kobieta,
        help_text="Płeć."
    )
    pets = models.ManyToManyField(
        Pet, 
        blank=True,        
        help_text="Wszystkie pupile przypisane do tego profilu."
    
    )

    created_at = models.DateTimeField(
        auto_now_add=True, 
        editable=False,
        verbose_name="Data rejestracji"
    )
    
    # Pupil jakiego szuka
    preferred_pet_type = models.CharField(
        max_length=1, 
        choices=PET_TYPES, 
        default='',        
        blank=True,        
        help_text="Jakiego puila szukasz u potencjalnego partnera."
    )

    bio = models.TextField(
        blank=True,
        help_text="Krótki opis o Was (Ty i Twój Pupil) i o tym, kogo szukasz."
    )

    # Obliczanie wieku na podstawie self.birth_date
def get_age(self): 
        pass


def __str__(self):
        pass
    
    # Krótki opis własny
bio = models.TextField(
        blank=True, 
        help_text="Krótki opis o Was (Ty i Twój Pupil) i o tym, kogo szukasz."
    )

def __str__(self):
        return f"Profil: {self.first_name} ({self.city})"


#Dopasowywanie (nie wiem czy to zadziala xd)
class Match(models.Model):
    """Model do śledzenia polubień i dopasowań między użytkownikami (Like = Match)."""
    
    swiper = models.ForeignKey( # jeden do wielu
        UserProfile, 
        on_delete=models.CASCADE, # jeśli profil zostanie usunięty, usuwamy też wszystkie polubienia i dopasowania
        related_name='given_likes', # kogo polubił
        verbose_name='Polubił'
    )
    
    target = models.ForeignKey(
        UserProfile, 
        on_delete=models.CASCADE, 
        related_name='received_likes', # kto polubił jego
        verbose_name='Polubiony'
    )
    
    is_match = models.BooleanField(default=False) # True, jeśli polubienie jest wzajemne
    timestamp = models.DateTimeField(auto_now_add=True) 

    def save(self, *args, **kwargs): 
        """Sprawdza, czy nastąpiło wzajemne polubienie (Match) i ustawia is_match=True."""
        super().save(*args, **kwargs) 

    class Meta:
        unique_together = ('swiper', 'target') # nie można polubić tej samej osoby dwa razy
        ordering = ['-timestamp'] #sortowanie od najnoszych

#Wiadomoci (tez nie wiem czy to bedzie dobrze)

class Message(models.Model):
    """Model do przechowywania wiadomości między dwoma dopasowanymi użytkownikami."""
    # Wiadomość musi być powiązana z dopasowaniem (zeby pisac tylko do matchy)
    match = models.ForeignKey(
        Match, 
        on_delete=models.CASCADE, 
        related_name='messages',
        help_text="Wiadomość powiązana z konkretnym dopasowaniem."
    )
    # Nadawca
    sender = models.ForeignKey(
        UserProfile, 
        on_delete=models.CASCADE, 
        related_name='sent_messages', 
        verbose_name='Nadawca'
    )
    #Odbiorca
    recipient = models.ForeignKey(
        UserProfile, 
        on_delete=models.CASCADE, 
        related_name='received_messages', 
        verbose_name='Odbiorca'
    )
    
    content = models.TextField(help_text="Treść wiadomości.") 
    timestamp = models.DateTimeField(auto_now_add=True) # Czas wysłania

    class Meta:
        ordering = ['timestamp'] # sortowanie od najstarszej dla historii czatu
        verbose_name = "Wiadomość"
        verbose_name_plural = "Wiadomości"