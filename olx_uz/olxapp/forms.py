from django import forms
from .models import Category, Advertisement, Comment
from django.core.exceptions import ValidationError

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control"
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if not name[0].isupper():
            raise ValidationError('Ismning bosh harfi katta harfda bolsihi kerak!!!')
        
class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        exclude = ['create_at']

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control"
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "image": forms.FileInput(attrs={
                "class": "form-control"
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if not title.isalpha():
            raise ValidationError('Nomi faqat harflardan iborat bolshi kerak!!!!')
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) >= 20:
            raise ValidationError('Tavsiv 20 ta harfdan kam bolsihi kerak!!!')
        return description
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']