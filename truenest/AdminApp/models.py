from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Property(models.Model):
    PROPERTY_TYPES = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
    ]
    PROPERTY_FOR = [
        ('for sell', 'For Sell'),
        ('for rent', 'For Rent'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    property_type = models.CharField(choices=PROPERTY_TYPES, max_length=20)
    property_for = models.CharField(choices=PROPERTY_FOR, max_length=20)
    location = models.CharField(max_length=255)
    beds = models.IntegerField(default=0)  
    baths = models.IntegerField(default=0) 
    garage = models.IntegerField(default=0) 
    sqft = models.PositiveIntegerField(default=0)  
    built_year = models.PositiveIntegerField(null=True, blank=True) 
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Latitude for map
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Longitude for map
    image = models.ImageField(upload_to='property_images/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
