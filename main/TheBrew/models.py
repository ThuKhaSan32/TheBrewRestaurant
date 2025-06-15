from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    STATUS_CHOICES = [
        ('normal', 'Normal'),
        ('diamond', 'Diamond'),
    ]

    name = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='normal')
    points = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name.username


class Log(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
    ]
    account = models.ForeignKey(Profile, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, default='login')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.name.username} - {self.action}"
    
class Menu(models.Model):
    image= models.ImageField(upload_to='menu_images/')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class PointRequest(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='point_requests/')
    points_requested = models.IntegerField()
    date_requested = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='pending')

    def __str__(self):
        return self.profile.name.username
