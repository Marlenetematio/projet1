from django.contrib.auth.forms import UserChangeForm , UserChangeForm
from django.forms import ModelForm
from .models import CustomUser

class EditUserprofileForm(UserChangeForm):

    class Meta:
        model= CustomUser
        fields ={ 'user_profile_image', 'username', 'firstname','lastname', 'email', 'user_bio', 'phone_number', 'competence_U'}




