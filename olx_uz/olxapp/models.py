from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def validate_description(value):
    if len(value) >= 40:
        raise ValidationError('Tavsif 40 ta harfadan kop bolmasin!!!!')
        
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(default='', max_length=40, validators=[validate_description])

    def __str__(self):
        return f"{self.name}"

class Advertisement(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
    
class Comment(models.Model):
    text = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    advertisment = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    edited = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user} {self.advertisment}"
    