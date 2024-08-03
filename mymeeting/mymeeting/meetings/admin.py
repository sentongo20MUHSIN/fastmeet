from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
class meetingAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    list_display = ("table_meeting", "agenda", "discussion", "action_items_decisions", "next_meeting_date", "created_at")
    summernote_fields = ('agenda', 'discussion', 'action_items_decisions')

  
admin.site.register(MeetingMinute, meetingAdmin)


class attendingAdmin(admin.ModelAdmin):
  list_display =  ("name","department","position","email","joined_at","meeting")
  
admin.site.register(Attending, attendingAdmin)

class tablemeetingAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    list_display = ("title", "date", "chair_meeting", "location", "description", "name", "email", "pdf_path")
    summernote_fields = ('description',)  #
  
admin.site.register(TableMeeting, tablemeetingAdmin)

