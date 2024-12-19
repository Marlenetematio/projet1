from django.contrib import admin

from django.urls import path , include
from . import views 



urlpatterns = [
    path('',views.home, name="home"),

    #Authentificqtion
    path('register',views.register, name="register"),
    path('login',views.logIn, name="login"),
    path('logout',views.logOut, name="logout"),
    path('activate/<uidb64>/<token>', views.activate , name="activate") ,
    path('contact',views.contact , name= "contact"),
     path('profile',views.profile, name="profile"),
    
    path('editprofile',views.UpdateUserView.as_view(), name="editprofile"),



    path('dashboard',views.dashboard , name="dashboard"),
    path('projets/', views.liste_projets, name='liste_projets'),
    
    path('create-task/', views.create_task, name='create_task'),
    path('gantt/', views.gantt_view, name='gantt_view'),
    
]