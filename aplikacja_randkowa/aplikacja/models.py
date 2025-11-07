from django.db import models

class Osoba(models.Model):
    PLEC_WYBOR = (
        ("K", "kobieta"),
        ("M", "mezczyzna"),
        ("I", "inna")
    )
    imie = models.CharField(max_length=50, null = False, blank = False)
    nazwisko = models.CharField(max_length=100, null = False, blank = False)
    plec = models.CharField(max_length=1, choices= PLEC_WYBOR, default= "I")
    
