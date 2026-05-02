from django.contrib import admin
from .models import Category, Advertisement, Comment, Advertister, Region

admin.site.register(Category)
admin.site.register(Advertisement)
admin.site.register(Comment)
admin.site.register(Advertister)
admin.site.register(Region)