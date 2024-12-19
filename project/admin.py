from django.contrib import admin
from .models import CustomUser,Projet, Tache
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Projet)
admin.site.register(Tache)