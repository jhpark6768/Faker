from django.contrib import admin
from phonebook.models import PhoneBook

# Register your models here.
class PhoneBookAdmin(admin.ModelAdmin):
    list_display = ('name','telnum','email','birth')

admin.site.register(PhoneBook, PhoneBookAdmin)