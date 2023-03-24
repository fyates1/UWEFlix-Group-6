from django.db import models
import datetime
from datetime import date
class screen(models.Model):
    name= models.CharField(max_length=256)
    capacity= models.IntegerField()
    # capacity = {array of 1 to 50}
    def __str__(self):
        return self.name

class row(models.Model):
    letter = models.CharField(max_length=256)
    screen = models.ForeignKey(screen, on_delete=models.CASCADE)
    def __str__(self):
        return f"Screen {self.screen}, row {self.letter}"

class seat(models.Model):
    number = models.IntegerField()
    row = models.ForeignKey(row,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.row},{self.number}"

class film(models.Model):
    title = models.CharField(max_length=256)
    #ageRating=models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    filmImage = models.ImageField(upload_to='images/')
    duration = models.CharField(max_length=6)
    ageSelection = (
        ("U", "U"),
        ("PG", "PG"),
        ("12A", "12A"),
        ("12", "12"),
        ("15", "15"),
        ("18", "18"),
    )

    age = models.CharField(choices=ageSelection, max_length=3)
    

    def __str__(self):
        return self.title 

class showing(models.Model):
    date= models.DateField("Date of showing (mm/dd/yyyy)")
    startTime=models.TimeField("Time of showing (HH:MM)")
    numberOfSales = models.IntegerField(blank=True, null=True)
    film=models.ForeignKey(film, on_delete=models.SET_NULL, null=True)
    screen= models.ForeignKey(screen,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.date},{self.film},{self.startTime}"