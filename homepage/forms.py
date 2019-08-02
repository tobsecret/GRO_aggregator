from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login, authenticate
from . import models
import datetime
import pytz
from pytz import timezone

class SignUpForm(forms.ModelForm): ##inherit from forms.ModelForm (standard forms from Django)
    password = forms.CharField(widget=forms.PasswordInput) #causes password field to be in ***
    email = forms.EmailField(required=True)

    class Meta: #meta data saying that this class will be a user class
        model = User
        fields = (  #what fields users will need
                'email',
                'password',
                'first_name',
                'last_name',)

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False) ##register as a ModelForm defined by Django
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email'] ##use the email as username cause you can't delete username field
        password = self.cleaned_data['password']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.set_password(password)
            user.save() #saves user to the database

        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email address is already registered')
        return email

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ('organization', 'occupation')

class LoginForm(forms.ModelForm): ##inherit from forms.ModelForm (standard forms from Django)
    password = forms.CharField(widget=forms.PasswordInput) #causes password field to be in ***
    email = forms.EmailField(required=True)


    class Meta: #meta data saying that this class will be a user class
        model = User
        fields = (  #what fields users will need
                'email',
                'password',
                )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email address is not registered')
        return email

    def clean_password(self):
        email = self.cleaned_data.get('email')
        nonHashPassword = self.cleaned_data.get('password')
        user = authenticate(username = email, password = nonHashPassword)
        if user is None:
            raise forms.ValidationError('Wrong password entered')
        return nonHashPassword
        
class CreateEvent(forms.ModelForm):
    submitter = forms.CharField(max_length=140,  widget = forms.HiddenInput(), required = False)
    date = forms.DateField(widget = forms.SelectDateWidget, initial=datetime.date.today())
    time = forms.TimeField(input_formats=['%I:%M %p'], widget=forms.TimeInput(format='%I:%M %p'), help_text = 'Format: Hour:Minute AM/PM')
    url = forms.URLField(max_length=200, widget=forms.TextInput, required = False)

    class Meta:
        model = models.Event
        fields = ['title', 'body', 'address', 'address2', 'city', 'state', 'price']

    def create(self):
        unaware_datetime = str(self.cleaned_data['date']) + " " + str(self.cleaned_data['time'])
        unaware_datetime = datetime.datetime.strptime(unaware_datetime, "%Y-%m-%d %H:%M:%S")
        localtime = timezone('US/Eastern')
        date_time = localtime.localize(unaware_datetime)
        NewEvent = models.Event.objects.create(
                    title = self.cleaned_data['title'],
                    body = self.cleaned_data['body'],
                    link = self.cleaned_data['url'],
                    date = date_time,
                    address = self.cleaned_data['address'],
                    address2 = self.cleaned_data['address2'],
                    city = self.cleaned_data['city'],
                    state = self.cleaned_data['state'],
                    price = self.cleaned_data['price'],
                    submitter = self.submitter,
                )
        NewEvent.save()
        return NewEvent


