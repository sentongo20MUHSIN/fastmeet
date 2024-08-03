# models.py
from django.db import models
from django_summernote.fields import SummernoteTextField
from django.db.models.functions import Lower
from django.db.models import UniqueConstraint

class TableMeeting(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField(null=True)
    chair_meeting = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    description = SummernoteTextField(blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    pdf_path = models.CharField(max_length=200, blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Attending(models.Model):
    meeting = models.ForeignKey(TableMeeting, on_delete=models.CASCADE, related_name='attendees')
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    joined_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    pdf_path = models.CharField(max_length=200, blank=True, null=True)  # Add this field

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.email = self.email.lower()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.name} attending {self.meeting.title}"
    
class MeetingMinute(models.Model):
    table_meeting = models.ForeignKey(TableMeeting, on_delete=models.CASCADE, related_name='minutes')
    agenda = SummernoteTextField(blank=True, null=True)
    discussion = SummernoteTextField(blank=True, null=True)
    action_items_decisions = SummernoteTextField(blank=True, null=True)
    next_meeting_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # is_pdf_enabled = models.BooleanField(default=False)
    def __str__(self):
        return f'Minutes for {self.table_meeting.title}'


