##this scrapper cannot scrap all the events; sometimes there is differences in the format of each page on eventbrite

from django.core.management.base import BaseCommand, CommandError
from homepage.models import Event
import requests
from bs4 import BeautifulSoup
import datetime
import pytz
from pytz import timezone

PendingEventList = []

possibleStreetNames = ["Road", "Way", "Street", "Avenue", "Boulevard" "Lane", "Drive", "Terrace", "Place", "Court", "Rd", " St", "Str", "Ave", "Av", "Blvd", "Ln", "Dr", "Pl"]

def month_converter(month):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(month) + 1

##possible div classes:
	##Event names in search page:
        ##("div", {"class": "eds-event-card__formatted-name--is-clamped"}) ##current one
		##("div", {"class": "event-card__formatted-name--is-clamped"})
		##("div", {"class": "card-text--truncated__three"})


class EventbriteObject:

    source = 'Eventbrite' ##this attributed will be shared by all objects

    def __init__(self, name, body, link, date_time, address, city, state, price): ##this is the constructor? allows calling EventbriteObject to make a new object
        self.name = name
        self.body = body
        self.link = link
        self.date_time = date_time
        self.address = address
        self.city = city
        self.state = state
        self.price = price

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

Eventbrite_url = "https://www.eventbrite.com/d/ny--new-york/biotech/?page="
pages = 10 ##number of pages on the above url to scrap

for pageNumber in range(1, pages + 1): ##add 1 to pages to get the right number of pages 

    siteinfo = requests.get(Eventbrite_url + str(pageNumber)) ##get html stuff for eventbrite page

    Eventbrite_soup = BeautifulSoup(siteinfo.content, features="html.parser") ##make it readable-ish

    Event_divs = Eventbrite_soup.find_all("section", {"class": "eds-l-pad-all-6 eds-media-card-content eds-media-card-content--list eds-media-card-content--standard eds-media-card-content--fixed"}) ##this is the div that is unique for each event and not duplicated
    
    for forLoopVar in Event_divs: ##go into each event div and pull out more specific info
        
        Name_html = forLoopVar.find_all("div", {"class": "eds-event-card__formatted-name--is-clamped"}) ##Name Of Event in div
        ##this class may loop twice in the page?
        name = Name_html[0].text
        print (name)

        Datetime_location_price_html = forLoopVar.find_all("div", {"class": "eds-text-bs--fixed eds-text-color--grey-600 eds-l-mar-top-1"})
        
        price = Datetime_location_price_html[2].text
        if price == 'Free':
            price = 0
        elif "at" in price: ##if price says Free or says nothing, just leave as is, but if event is not free, split the string at " at " and just get the number to put in price
            price = price.split(" at ")[1]
            ##.replace removes all commas in the price string
            
            price = float(price.replace(',', '')[1:]) ##make the price into a float number; price[1:] removes the '$' sign
            ##print(price)
        else:
            price = None
        Link_html = forLoopVar.find_all("a", {"tabindex": 0})
        link = Link_html[0].get("href")

        specificEventLink = requests.get(link) ##open the eventbrite page for that event (mainly to get the event details)
        specificEvent_soup = BeautifulSoup(specificEventLink.content, features="html.parser")
        eventpagetype = specificEvent_soup.find_all("body", {"id": "page_eventview"}) ##There's a different type of pages for certain events called page_eventview; didn't have time to make this type of scrapper yet so just skip these
        if len(eventpagetype) == 0: ##if len(eventpagetype) == 1, it means its the other event page type, so just skip those for now

            Body_html = specificEvent_soup.find_all("div", {"class": "js-xd-read-more-contents l-mar-top-3"})
            if not Body_html: ##skip to the next event if body_html cannot be found
                print("Cannot find body")
                continue
            ##print (Body_html)
            body_list = Body_html[0].text.rstrip().split("\n") ##split by newline characters in the body text
            body = ''

            for eachline in body_list: ##add each line of the event body back without the new lines
                if len(eachline) > 3: ##if the line is just a space or just too short, skip these lines
                    body = body + eachline + " "
                    if "  " in body[-2:]: ##if end of the line contains two spaces
                        body = body[:-2] + "\n" ##get the line up until the last two characters and add a new line
                if len(body) > 500: ##if the body exceeds 500 characters, just use the first 500 characters
                    break
            body = body[:-1] ##remove the last space in the body

            Datetime_Location_html = specificEvent_soup.find_all("div", {"class": "event-details__data"}) ##div containing the datetime in the first index and location in the second index of the specific event page
            datetime_list = Datetime_Location_html[0].text.rstrip().split(",")
            month = month_converter(datetime_list[1][1:4]) ##get the 2nd element in the array and just get the first 3 letters of the month
            date = datetime_list[1].split(" ")[2] ##get the 2nd element in the array for the date
            year = datetime_list[2][1:5]
            hour = "00"
            minute = "00"
            Day_N_Nite = "PM"
            if len(datetime_list) > 3: ##if want to see what indices these are and what positions of these characters, just print them out
                hour_min_split = datetime_list[3].split(" ")
                hour = hour_min_split[1].split(":")[0]
                minute = hour_min_split[1].split(":")[1]
                Day_N_Nite = hour_min_split[2]
            else:
                year_time_split = datetime_list[2].split("\n")
                year = year_time_split[0][1:5] ##get 1st element in the array and the 2nd to 5th characters in the string to get the year
                hour = year_time_split[1].split(":")[0]
                minute = year_time_split[1].split(":")[1][0:2]
                Day_N_Nite = year_time_split[1].split(":")[1][3:5]
            unaware_datetime = str(year) + "-" + str(month) + "-" + str(date) + " " + str(hour) + ":" + str(minute) + " " + str(Day_N_Nite)
            unaware_datetime = datetime.datetime.strptime(unaware_datetime, "%Y-%m-%d %I:%M %p")
            localtime = timezone('US/Eastern')
            date_time = localtime.localize(unaware_datetime)

            location_list = Datetime_Location_html[1].text.rstrip().split("\n") ##split location by new line (splits the address, city, state, "View Map",etc)
            address = location_list[1] ##use the 1st line of the location as the address; however, this may not always list an actual address with building number and street name

            for yellowpages in location_list: ##loops through the "address" provided by eventbrite and picks the line that contains a generic street name word like "Street" or "Avenue" and a building number
                if hasNumbers(yellowpages):
                    if any(streetNames in yellowpages for streetNames in possibleStreetNames):
                        address = yellowpages
                        break ##leave loop when the correct address line is found
            ##print(location_list[-4])
            
            city = location_list[-4].split(",")[0] ##get the city by splittings the "City, State Zip code" line by comma
            state = location_list[-4] ##use the zipcode if the address only contains the zip code
            if len(location_list[-4]) > 6:
                state = location_list[-4].split(", ")[1][0:-6] ##get the 2nd element of the split and grab the string of the first element to just before the zip code
            ##state = location_list[-4][-9:-7] ##get the 4th element from the back of the split array and then get the substring using reverse index to get the state
            ##if state.islower(): ##if the string of state is lower case (not a state), go into if statement
            ##    state = " ".join(location_list[-4].split(" ")[1:-2]) ##split address string by spaces and get the middle to second to last elements
                ##join the list into a string separated by space
            ##print(state)

            PendingEventList.append(EventbriteObject(name, body, link, date_time, address, city, state, price)) ##add each event object into the pending event list

class Command(BaseCommand): ##need to add restriction for duplicate events
    help = 'This is a scrapper written by Vincent Tu'
    def handle(self, *args, **options): ##what do these arguments mean?
        for EventObjects in PendingEventList:
            ##UTCtime = EventObjects.date_time.astimezone(pytz.utc) ##converts the datetime back to UTC
            if len(Event.objects.filter(title = EventObjects.name, date = EventObjects.date_time, address = EventObjects.address)) < 1: ##search for events with the same name, time, and location in the database; if an event is found to contain the same name, time, and location, don't add it to the database; this does not work for admin - created events for some reason. the scrapper will add evenets of the same name, time, and location as an admin created one
                NewEvent = Event.objects.create(
                    title = EventObjects.name,
                    body = EventObjects.body,
                    link = EventObjects.link,
                    date = EventObjects.date_time,
                    address = EventObjects.address,
                    city = EventObjects.city,
                    state = EventObjects.state,
                    price = EventObjects.price,
                    submitter = EventObjects.source
                ) ##create events in django model based on the Event class written here
                NewEvent.save() ##dont this we need this line. the create function might already save each object into the database




