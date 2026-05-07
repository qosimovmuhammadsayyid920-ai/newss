from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def validate_description(value):
    if len(value) >= 40:
        raise ValidationError('Tavsif 40 ta harfadan kop bolmasin!!!!')

class Region(models.Model):
    region_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Joylashuv nomi')

    def __str__(self):
        return f"{self.region_name}"
    
    class Meta:
        verbose_name = 'Joylashuv'
        verbose_name_plural = 'Joylashuvlar'
        ordering = ('region_name',)
    
class Advertister(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ismi')
    phone_number = models.CharField(max_length=15, default="+998", unique=True, null=True, blank=True, verbose_name='Telefon raqam')

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = 'Elon Joylovchi'
        verbose_name_plural = 'Elon Joylovchilar'
        ordering = ('name',)
        
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Bolim nomi')
    description = models.CharField(default='', max_length=40, validators=[validate_description], verbose_name='Tavsif')

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = 'Bolim'
        verbose_name_plural = 'Bolimlar'
        ordering = ("name",)

class Advertisement(models.Model):
    advertisters = models.ManyToManyField(Advertister, related_name='advertister', verbose_name='Elon joylovchi')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Joylashuv')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Bolim')
    title = models.CharField(max_length=200, verbose_name='Nomi')
    description = models.TextField(verbose_name='Izoh')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Narxi')
    image = models.ImageField(upload_to='images/', verbose_name='Rasm', null=True, blank=True)
    video = models.FileField(upload_to='video/', verbose_name='Video', null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        verbose_name = 'Elon'
        verbose_name_plural = 'Elonlar'
        ordering = ('title', '-create_at')

class Comment(models.Model):
    text = models.CharField(max_length=100, verbose_name='Izoh')
    created = models.DateTimeField(auto_now_add=True)
    advertisment = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} {self.advertisment}"
    
    def save(self, *args, **kwargs):  # to'g'ri signature
        if self.pk:
            old = Comment.objects.get(pk=self.pk)
            if old.text != self.text:
                self.edited = True
        super().save(*args, **kwargs)
    
    
    class Meta:
        verbose_name = 'Izox'
        verbose_name_plural = 'Izoxlar'

class BookMark(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} -> {self.advertisement}"