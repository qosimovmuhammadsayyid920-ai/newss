from django.contrib import admin
from .models import Category, Advertisement, Comment, Advertister, Region
from django.utils.safestring import mark_safe

admin.site.site_header = ('Elon Uz')
admin.site.site_title = ('Elon Uz')
admin.site.login_template = 'admin/login.html'
admin.site.logout_template = 'admin/logout.html'

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    exclude = ('user',)
    readonly_fields = ('edited',)

@admin.register(Advertisement)
class AdvertismentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'get_video',]
    list_filter = ('category', 'advertisters',)
    list_editable = ('category', 'price',)
    search_fields = ('title', 'category__name',)
    fieldsets = [
        (
            "Elon xaqida",
            {
                'fields': ['category', 'title', 'advertisters'],
            }
        ),
        (
            "Qoshimcha",
            {
                'fields': ['region', 'description'],
                'classes': ['collapse']
            }
        ),
        (
            "Narx",
            {
                'fields': ['price']
            }
        ),
        (
            "Medialar",
            {
                'fields': ['image', 'video']
            }
        )

    ]
    inlines = [
        CommentInline
    ]

    @admin.display(description="Rasmi")
    def get_video(self, advertisment):
        if advertisment.video:
           return mark_safe(f'<video src="{advertisment.video.url}" width="100px" style="border-radius: 30%;" controls></video')
        else:
            return '-'

    def save_formset(self, request, form, formset, change):
        isinstance = formset.save(commit=False)
        for obj in isinstance:
            if not obj.user:
                obj.user = request.user
            obj.save()
        formset.save_m2m()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Advertister)
class AdvertisterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number',)

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass