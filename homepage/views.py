from django.shortcuts import render, redirect
from django.views.generic import ListView, View ##allows listing of basic views
from homepage.models import Event
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm, CreateEvent
from django.contrib.auth.decorators import login_required
from .utils import Calendar
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta, date
import calendar

def index(request):
    event_list = Event.objects.filter(display = True)
    context = {'event_list': event_list} #passes events from Event model to home.html
    return render (request, 'homepage/home.html', context) #The render() function takes the request object as its first argument, a template name as its second argument and a dictionary as its optional third argument (which is called context in this line)

class EventListView(ListView):
    model = Event
    template_name = 'homepage/home.html'
    context_object_name = 'event_list'
    ordering = ['date']
    paginate_by = 5

def contact(request):
    contactsContent = {
           'content': ['If you would like to contact GRO, please email GRObiotech@gmail.com'],
           'title': 'Contact'
    }
    return render(request, 'homepage/contact.html', contactsContent) #'content' is the dictionary that is defined in the render line; it points to the things in bracket when 'content is called'

class CalendarView(ListView):
    model = Event
    template_name = 'homepage/calendar.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None)) ##uses the get_date function defined below
        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)
        cal.setfirstweekday(6) ##set the first day of the week to Sunday
        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d) ##uses the prev_month function defined below
        context['next_month'] = next_month(d)
        return context

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data['email']
            nonHashPassword = form.cleaned_data['password'] ##clean up the password entered into the form password field
            user = authenticate(username = email, password = nonHashPassword) ##login the user after sign up; use request.POST password instead of user.password because the user will spit out a hash algorithm for the password
            
            if user is not None:
                if user.is_active: ##if they're not banned
                    login(request, user)
                    return redirect('/')
        return render(request, 'homepage/signup_form.html', {'form': form, 'title': 'Sign Up'}) #return to blank form if form is not valid
    else:
        form = SignUpForm()
        return render(request, 'homepage/signup_form.html', {'form': form, 'title': 'Sign Up'})
    
    
def gro_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            nonHashPassword = form.cleaned_data['password'] ##clean up the password entered into the form password field
            user = authenticate(username = email, password = nonHashPassword) ##login the user after sign up; use request.POST password instead of user.password because the user will spit out a hash algorithm for the password
            
            if user is not None:
                if user.is_active: ##if they're not banned
                    login(request, user)
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    else:
                        return redirect('/')

        return render(request, 'homepage/login_form.html', {'form': form, 'title': 'Login'}) #return to blank form if form is not valid
    else:
        form = LoginForm()
        return render(request, 'homepage/login_form.html', {'form': form, 'title': 'Login'})

def gro_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')


@login_required(login_url="/login/")
def create_event(request):
    if request.method == 'POST':
        form = CreateEvent(request.POST)
        if form.is_valid():
            form.submitter = request.user.username
            form.create()
            print(form.submitter)
            return redirect('/')
        return render(request, 'homepage/create_event.html', {'form':form, 'title': 'Create Event'})
    else:
        form = CreateEvent()
        return render(request, 'homepage/create_event.html', {'form':form, 'title': 'Create Event'})
    