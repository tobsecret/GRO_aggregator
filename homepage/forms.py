from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login

class UserForm(forms.ModelForm): ##inherit from forms.ModelForm (standard forms from Django)
    password = forms.CharField(widget=forms.PasswordInput) #causes password field to be in ***
    email = forms.EmailField(required=True)


    class Meta: #meta data saying that this class will be a user class
        model = User
        fields = (  #what fields users will need
                'username', 
                'email', 
                'first_name',
                'last_name',
                'password')

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False) ##register as a ModelForm defined by Django
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if commit:
             user.save() #saves user to the database
             user.set_password(password)

        return user
#           
