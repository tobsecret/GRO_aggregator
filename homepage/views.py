from django.shortcuts import render, redirect
from django.views.generic import ListView, View ##allows listing of basic views
from homepage.models import Event
from django.contrib.auth import authenticate, login
from .forms import UserForm ##UserForm is the Django template for user signups

def index(request):
    event_list = Event.objects.all()
    context = {'event_list': event_list} #passes events from Event model to home.html
    return render (request, 'homepage/home.html', context) #The render() function takes the request object as its first argument, a template name as its second argument and a dictionary as its optional third argument (which is called context in this line)

def contact(request):
    return render(request, 'homepage/contact.html', {'content':['If you would like to contact GRO, please email', 'GRObiotech@gmail.com']}) #'content' is the dictionary that is defined in the render line; it points to the things in bracket when 'content is called'

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'homepage/signup_form.html', {'form': form}) #return to blank form if form is not valid
    else:
        form = UserForm()
        return render(request, 'homepage/signup_form.html', {'form': form})



