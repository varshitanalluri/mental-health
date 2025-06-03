from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [('parent', 'Parent'), ('child', 'Child')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    linked_parent = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return f'{self.user.username} - {self.role}'

class StressResult(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stress_level = models.CharField(max_length=20) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ESP32Data(models.Model):
    heart_rate = models.IntegerField()
    spo2 = models.IntegerField()
    steps = models.IntegerField()
    temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"HR: {self.heart_rate}, SpO2: {self.spo2}, Temp: {self.temperature}"
    
