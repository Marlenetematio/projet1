from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from projet_soutenance import settings
from django.utils.http  import urlsafe_base64_decode , urlsafe_base64_encode
from django.utils.encoding import  force_text
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .token import generatorToken
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.urls import reverse_lazy
from django.core.mail import send_mail , EmailMessage
from django.views.generic import ListView
from .forms import  EditUserprofileForm
from .models  import    CustomUser ,Projet,Tache
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission

from django_jquery_datatables.utils import JqueryDatatable
from rest_framework import serializers
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json




def home (request):
    return render(request,'home.html')

def register(request):
    if request.method == "POST":
        username =request.POST['username']
        firstname =request.POST['firstname']
        lastname =request.POST['lastname']
        email =request.POST['email']
        phone_number =request.POST['phone_number']
        user_bio =request.POST['user_bio']
        user_profile_image=request.POST['user_profile_image']
        competence_U=request.POST['competence_U']
        password =request.POST['password']
        password1 =request.POST['password1']
        if CustomUser.objects.filter(username=username):
            messages.error(request, "Ce nom a ete deja pris")
            return redirect('register')
        if CustomUser.objects.filter(email=email ): 
            messages.error(request, "Cet email a deja un compte")
            return redirect('register')
        
        if password != password1 :
            messages.error(request, "Les deux password ne coincident pas")
            return redirect('register')
        mon_utilisateur = CustomUser.objects.create(email=email, password=password, username=username)
        mon_utilisateur.firstname = firstname
        mon_utilisateur.lastname = lastname
        mon_utilisateur.phone_number = phone_number
        mon_utilisateur.user_bio = user_bio
        mon_utilisateur.user_profile_image = user_profile_image
        mon_utilisateur.competence_U = competence_U
        mon_utilisateur.is_active = False
        mon_utilisateur.save()
        messages.success(request, 'Votre compte a été crée avec succes')
        # Envoi d'email de bienvenu
        subject='Bienvenu sur pro django system login'
        message = 'Bienvenu'+ mon_utilisateur.firstname + " " + mon_utilisateur.lastname + "\n Nous sommes heureux de vous compter parmi nous\n\n\n Merci \n\n M@rlene Web master"
        from_email= settings.EMAIL_HOST_USER
        to_list=[mon_utilisateur.email] 
        send_mail(subject, message, from_email , to_list , fail_silently=False)
# Email de confimation   
        current_site =get_current_site(request)
        email_subject = " Confirmation de l'adresse email"
        messageConfirm = render_to_string("emailconfirm.html",{
            "name": mon_utilisateur.firstname,
            'domain': current_site.domain , 
            'uid': urlsafe_base64_encode(force_bytes(mon_utilisateur.pk)),
            'token':generatorToken.make_token(mon_utilisateur)

        })
        email= EmailMessage(
            email_subject,
            messageConfirm,
            settings.EMAIL_HOST_USER,
            [mon_utilisateur.email]

        )
        
        email.send()


        return redirect ('login')
    return render(request, 'register.html')


def logIn(request):
    if request.method == "POST":
        email =request.POST['email']
        password =request.POST['password']
        try:
            my_user=CustomUser.objects.get(email= email)
        except:
            messages.error(request,"Compte inexistant")
            return redirect('login')
        user = authenticate(email=email , password=password)
        if my_user.password == password or user is not None:
            login(request,my_user)
            return redirect('dashboard')
        elif my_user.is_active == False:
            messages.error(request,"vous n'avez pas confirmé votre adresse mail , faites le avant de de vous connecter  merci")
        
        else:
           messages.error(request,'mauvaise authentification')
           return redirect('login')
    return render(request, 'login.html')

def logOut(request):
    logout(request) 
    messages.success(request,'Vous etes deconnecté')
    return redirect('home')
def activate(request,uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user =CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and generatorToken.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'votre compte a ete activé, félicitation Connectez vous maintenant!!!')
        return redirect('login')
    else:
        messages.error(request, 'Activation echouée !!! Veuillez réessayer!!!')
        return redirect('home')


@login_required 
def dashboard(request):
    return render(request,'dashboard.html')
def contact(request):
    return render(request, 'contact.html')
@login_required
    
def profile(request):
    return render(request, 'profile.html')

class UpdateUserView(generic.UpdateView):
    form_class = EditUserprofileForm
    template_name = "profile.html"
    success_url= reverse_lazy('profile')
    def get_object(slef):
        return slef.request.user


# Create your views here.
def liste_projets(request):
    projets = Projet.objects.all()
    return render(request, 'projets/liste_projets.html', {'projets': projets})

def assign_permissions():
    # Exemple de création d'un groupe et d'une permission
    groupe_chef = Group.objects.create(name='Chef de projet')
    permission_chef = Permission.objects.get(codename='can_gerer_projets')
    groupe_chef.permissions.add(permission_chef)







def gantt_view(request):
   projets = Projet.objects.all()
   taches = Tache.objects.all()
   return render(request, 'gantt.html', {'projets': projets, 'taches': taches})

def create_task(request):
    # Logique pour créer une tâche à partir des données envoyées
    return JsonResponse({'status': 'success'})

