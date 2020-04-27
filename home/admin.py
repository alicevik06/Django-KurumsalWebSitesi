from django.contrib import admin

# Register your models here.
from home.models import Setting, ContactFormMessages

class ContactFormMessagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message', 'note', 'status']
    list_filter = ['status']

admin.site.register(ContactFormMessages,ContactFormMessagesAdmin)
admin.site.register(Setting)