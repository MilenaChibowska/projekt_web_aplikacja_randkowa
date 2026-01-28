from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint, Q
from datetime import date




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


GENDER_CHOICES = models.IntegerChoices(
    'Płeć',
    'Kobieta Mężczyzna Inna Nie podano'
)


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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

    def get_age(self):
        if not self.birth_date:
            return "Nie podano"
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
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

    def __str__(self):
            return f"Profil: {self.first_name} ({self.city})"


class Match(models.Model):
    
    swiper = models.ForeignKey( 
        UserProfile, 
        on_delete=models.CASCADE, 
        related_name='given_likes', 
        verbose_name='Polubił'
    )
    
    target = models.ForeignKey(
        UserProfile, 
        on_delete=models.CASCADE, 
        related_name='received_likes',
        verbose_name='Polubiony'
    )
    
    is_match = models.BooleanField(default=False) 
    timestamp = models.DateTimeField(auto_now_add=True) 

    def save(self, *args, **kwargs): 
        super().save(*args, **kwargs) 

    class Meta:
        unique_together = ('swiper', 'target') 
        ordering = ['-timestamp'] 


class Message(models.Model):   
    match = models.ForeignKey(
        Match, 
        on_delete=models.CASCADE, 
        related_name='messages',
        help_text="Wiadomość powiązana z konkretnym dopasowaniem."
    )
    
    sender = models.ForeignKey(
        UserProfile, 
        on_delete=models.CASCADE, 
        related_name='sent_messages', 
        verbose_name='Nadawca'
    )
    
    recipient = models.ForeignKey(
        UserProfile, 
        on_delete=models.CASCADE, 
        related_name='received_messages', 
        verbose_name='Odbiorca'
    )
    
    content = models.TextField(help_text="Treść wiadomości.") 
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        verbose_name = "Wiadomość"
        verbose_name_plural = "Wiadomości"