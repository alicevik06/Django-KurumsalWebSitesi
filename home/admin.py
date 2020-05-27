from django.contrib import admin

# Register your models here.
from home.models import Setting, ContactFormMessages, UserProfile, SSS


class ContactFormMessagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message', 'note', 'status']
    list_filter = ['status']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'ogrencino', 'phone', 'address', 'city', 'country', 'image_tag']


class SSSAdmin(admin.ModelAdmin):
    list_display = ['Snumber', 'question', 'answer', 'status']
    list_filter = ['status']

admin.site.register(ContactFormMessages,ContactFormMessagesAdmin)
admin.site.register(Setting)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(SSS, SSSAdmin)