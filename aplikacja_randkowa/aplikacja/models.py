from django.db import models

PLEC_WYBOR = (
    ("K", "kobieta"),
    ("M", "mezczyzna"),
    ("I", "inna")
)

class Osoba(models.Model):

    imie = models.CharField(max_length=50, null = False, blank = False)
    nazwisko = models.CharField(max_length=100, null = False, blank = False)
    plec = models.CharField(max_length=1, choices= PLEC_WYBOR, default= "I")
    
