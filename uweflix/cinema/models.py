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
    film=models.ForeignKey(film, on_delete=models.RESTRICT, null=True)
    screen= models.ForeignKey(screen,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.date},{self.film},{self.startTime}"
    
    
class Booking(models.Model):
    bookingID = models.AutoField(primary_key=True,unique=True)
    showing = models.ForeignKey(showing, on_delete=models.CASCADE, null=True)
    student_tickets = models.IntegerField(default=0)
    child_tickets = models.IntegerField(default=0)
    adult_tickets = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    # created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.bookingID},{self.showing},{self.student_tickets},{self.child_tickets},{self.adult_tickets},{self.total_price}"
