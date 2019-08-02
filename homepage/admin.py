from django.contrib import admin
from homepage.models import Event, UserProfile

class EventDisplays(admin.ModelAdmin): ##set what info to display on Events section
    list_display = ('title', 'displayed', 'date', 'address', 'view_link') ##view_link is defined in models.py to show clickable link; can add 'Action' for checkbox, once it's troubleshooted
    list_filter = ('title', 'date', 'city', 'displayed') ##adds a filtering option'
    actions = ('update', 'deupdate', 'delete')

    def update(self, request, queryset): ##dropdown menus in admin page to add events to homepage
        events_updated = queryset.update(displayed=True)
        if events_updated == 1:
            message_bit = "One event was"
        else:
            message_bit = "%s events were" % events_updated
        self.message_user(request, "%s successfully updated." % message_bit) ##give message to user
    update.short_description = "Display selected events to Homepage"

    def deupdate(self, request, queryset):
        events_removed = queryset.update(displayed=False)
        if events_removed == 1:
            message_bit = "One event was"
        else:
            message_bit = "%s events were" % events_removed
        self.message_user(request, "%s successfully removed." % message_bit) ##give message to user
    deupdate.short_description = "Remove selected events from display on Homepage"

class ProfileDisplays(admin.ModelAdmin): ##set what info to display on Profiles section
    list_display = ('user', 'email', 'first_name', 'last_name', 'organization', 'occupation')
    list_filter = ('email', 'organization', 'occupation') ##adds a filtering option'
    
    def get_actions(self, request): ##remove the delete button on UserProfile page
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    class Media:
        css = {
            'all': ('css/admin_user_editing_buttons.css',)
        }


admin.site.register(Event, EventDisplays) ##loads Event classes in models file into database
admin.site.register(UserProfile, ProfileDisplays)

admin.site.site_header= 'GRO Admin Superpowers'

# Register your models here.

