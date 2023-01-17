from django.contrib import admin
from .models import *

class PetAdmin(admin.ModelAdmin):
    list_display = ('nome', 'status')

admin.site.register(Raca)
admin.site.register(Tag)
admin.site.register(Pet, PetAdmin)