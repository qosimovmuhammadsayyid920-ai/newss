from django.contrib import admin
from .models import Category, Advertisement, Comment, Advertister, Region

admin.site.site_header = ('Elon Uz')
admin.site.site_title = ('Elon Uz')
admin.site.login_template = 'admin/login.html'
admin.site.logout_template = 'admin/logout.html'

admin.site.register(Category)
admin.site.register(Advertisement)
admin.site.register(Comment)
admin.site.register(Advertister)
admin.site.register(Region)