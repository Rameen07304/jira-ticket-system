
from django.db import models
from django.contrib.auth.models import User
CITY_CHOICES = [
    ('KHI', 'Karachi'),
    ('LHR', 'Lahore'),
    ('ISB', 'Islamabad'),
    ('NYC', 'New York City'),
    ('LON', 'London'),
    ('DEL', 'Delhi'),
    ('TKY', 'Tokyo'),
    ('SYD', 'Sydney'),
]

COUNTRY_CHOICES = [
    ('PK', 'Pakistan'),
    ('IN', 'India'),
    ('US', 'United States'),
    ('UK', 'United Kingdom'),
    ('JP', 'Japan'),
    ('AU', 'Australia'),
]

class CustomUser(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE )
    dob=models.DateField(help_text="Enter date in the format YYYY-MM-DD (e.g., 1990-06-30)", null=True, blank=True)
    city = models.CharField(max_length=50, choices=CITY_CHOICES,null=True, blank=True)
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, null=True, blank=True)
    pincode = models.CharField(max_length=10,null=True, blank=True)
    address = models.TextField(default='No address provided', null=True, blank=True)


    def __str__(self):
        return self.user.username
    
    