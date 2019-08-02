from django.db import models
import geocoder ##for geocoding addresses
from django.core.validators import RegexValidator ##a validator for the text fields
from django.utils.html import format_html ##allow html format
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Event(models.Model):
    title = models.CharField(max_length=140)
    body = models.TextField(blank=True)
    link = models.URLField(max_length=140, blank=True, null = True)
    date = models.DateTimeField()
    address = models.CharField(max_length=140, validators=[RegexValidator(regex = '^[a-zA-Z0-9 .-]+$', message = 'Enter only letters or numbers for address')])
    address2 = models.CharField(max_length=140, blank=True)
    city = models.CharField(max_length=140, default='')
    state = models.CharField(max_length=2, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2, blank = True, null = True)
    longitude = models.DecimalField(max_digits = 13, decimal_places = 10, blank = True, null = True, editable = False)
    latitude = models.DecimalField(max_digits = 13, decimal_places = 10, blank = True, null = True, editable = False)
    displayed = models.BooleanField(default=False, editable = False) ##checkbox value to show on homepage or not
    submitter = models.CharField(max_length=140, default='') ##allows admin to sort by User submitted events or scraped events 

    class Meta:
        ordering = ["date"]

    def view_link(self): ##allows link to be shown on the admin page
        if (self.link is "") or (self.link is None):
            return format_html(
                    u'<a>%s</a>' % (str(self.submitter))
            )
        else:
            return format_html(
                    u'<a href="%s">%s</a>' % (self.link, str(self.submitter))
            )
    view_link.short_description = 'Submitter'
    view_link.allow_tags = True
    
    def mapcallback(self):
        callback = 'mapcallback' + str(self.id) ##this function allows leaflet to call individual functions to initiate the map, based on the event's id
        return callback

    ##def Action(self): ##add a button to admin events page to select events for display
    ##    return format_html(
    ##            '<form method="post"><input id="{{status}}" type="checkbox" name="{{status}}"></form>'
    ##    )
    ##Action.short_description = 'On homepage' ##name of the column

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        LatLng = geocoder.osm(self.address + ", " + self.city + " " + self.state + " USA").latlng ##get latitude and longitude coordinates for NYC addresses
        if LatLng is None: ##if this address returns a None object (cause its nonsense)
            CityLatLng = geocoder.osm(self.city + ", " + self.state + " USA").latlng ##geocode the city
            if CityLatLng is not None:
                self.longitude = float(CityLatLng[1:2][0]) ##return coordinates of the city if geocoder cannot find address
                self.latitude = float(CityLatLng[0:1][0])
            else: ##otherwise if the city and state is still a none object
                self.longitude = float(geocoder.osm("New York, NY").latlng[1:2][0]) ##just return NYC for the map
                self.latitude = float(geocoder.osm("New York, NY").latlng[0:1][0])
        else:
            self.longitude = float(LatLng[1:2][0])
            self.latitude = float(LatLng[0:1][0]) ##return the reversed coordinates in Longitude and Latitude format (for OSM Maps)
        super(Event, self).save(*args, **kwargs)

class UserProfile(models.Model): ##defines a User model so Django can save User fields like organization and occupation; extends Django User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(default='', blank=True)
    first_name = models.CharField(max_length=50, default='', blank=True)
    last_name = models.CharField(max_length=50, default='', blank=True)
    organization = models.CharField(max_length=50, default='', blank=True)
    occupation = models.CharField(max_length=50, default='', blank=True)
    
    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()