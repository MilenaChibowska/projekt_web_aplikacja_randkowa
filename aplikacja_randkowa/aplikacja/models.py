from django.db import models
from django.contrib.auth.models import User
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

GENDER_CHOICES = (
    (1, 'Kobieta'),
    (2, 'Mężczyzna'),
    (3, 'Inna'),
    (4, 'Nie podano'),
)


class Pet(models.Model):
    name = models.CharField(max_length=50, help_text="Imię zwierzaka.", verbose_name="Imie pupila")
    pet_type = models.CharField(max_length=1, choices=PET_TYPES, default='', help_text="Typ zwierzaka.")
    breed = models.CharField(max_length=100, blank=True, help_text="Rasa pupila.")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Waga w kg")
    description = models.TextField(blank=True, help_text="Opis pupila.")
    is_friendly = models.BooleanField(default=True, help_text="Czy przyjazny?")
    age = models.PositiveSmallIntegerField(default=1, help_text="Wiek.")

    def __str__(self):
        return f"{self.name} ({self.get_pet_type_display()})"
    
    class Meta:
         verbose_name="Pupil"
         verbose_name_plural = "Pupile"
         ordering = ['name'] 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1)
    pets = models.ManyToManyField(Pet, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    preferred_pet_type = models.CharField(max_length=1, choices=PET_TYPES, default='', blank=True)
    bio = models.TextField(blank=True)

    def get_age(self):
        if not self.birth_date: return "Nie podano"
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def __str__(self):
        imie = self.first_name or "Brak"
        miasto = self.city or "Brak"
        return f"Profil: {imie} ({miasto})"

class Match(models.Model):
    swiper = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='given_likes', verbose_name='Polubił')
    target = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_likes', verbose_name='Polubiony')
    is_match = models.BooleanField(default=False) 
    timestamp = models.DateTimeField(auto_now_add=True) 

    class Meta:
        unique_together = ('swiper', 'target') 
        ordering = ['-timestamp'] 

class Message(models.Model):   
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField() 
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']