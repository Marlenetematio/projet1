from django.db import models

# Create your models here.
from typing import Any
from django.db import models
from datetime import datetime , timedelta
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser 
from .manager import Usermanager
from django.contrib.auth.models import PermissionsMixin

class CustomUser(AbstractBaseUser, PermissionsMixin):
   username =models.CharField( max_length=50 , unique=True,blank=True, null=True)
   firstname = models.CharField( max_length=50 ,blank=True, null=True)
   lastname= models.CharField(max_length=50,blank=True, null=True)
   email = models.EmailField(unique=True)
   phone_number = models.CharField( max_length=50 , unique=False ,blank=True, null=True)
   user_bio= models.CharField( max_length=50,blank=True, null=True)
   user_profile_image= models.ImageField( upload_to="document",blank=True, null=True)
   competence_U=models.TextField(blank=True, null=True)

   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = []
   objects = Usermanager()

   is_active = models.BooleanField(default=False)
   is_superuser = models.BooleanField(default=False)
   is_staff= models.BooleanField(default=False)
   models.DateTimeField(default=timezone.now )

   def __str__(self):
         return f"{ self.lastname} {self.firstname}"
   
class Projet(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    chef_de_projet = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nom

class Tache(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    statut = models.CharField(max_length=20, choices=[
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée')
    ])
    date_echeance = models.DateField()
    projet = models.ForeignKey(Projet, related_name='taches', on_delete=models.CASCADE)
    affecte_a = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.titre
class Commentaire(models.Model):
    tache = models.ForeignKey(Tache, related_name='commentaires', on_delete=models.CASCADE)
    auteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    texte = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire sur {self.tache.titre} par {self.auteur.username}"