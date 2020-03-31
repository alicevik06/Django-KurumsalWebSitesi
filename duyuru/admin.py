from django.contrib import admin

# Register your models here.
from duyuru.models import Category, Duyuru, Images
class DuyuruImageInline(admin.TabularInline):
    model = Images
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status','image_tag']
    readonly_fields = ('image_tag',)
    list_filter = ['status']

class DuyuruAdmin(admin.ModelAdmin):
    list_display = ['title','category', 'image_tag','status','update_at']
    readonly_fields = ('image_tag',)
    list_filter = ['status','category']
    inlines = [DuyuruImageInline]


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'duyuru','image_tag']
    readonly_fields = ('image_tag',)

admin.site.register(Category,CategoryAdmin)
admin.site.register(Duyuru,DuyuruAdmin)
admin.site.register(Images,ImagesAdmin)