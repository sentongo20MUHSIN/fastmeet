# forms.py
from django.utils import timezone

from django import forms
from .models import TableMeeting, Attending, MeetingMinute
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            return name.upper()
        return name

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            return email.lower()
        return email
class TableMeetingForm(forms.ModelForm):
    class Meta:
        model = TableMeeting
        fields = ['title','date','chair_meeting', 'location','description']
        labels = {
            'title': 'Title For Meeting:',
            'date': 'Date and Time',
            'chair_meeting': 'Chair OF The Meeting:',
            'location': 'Location',
            'description': 'Purpose',
            #'name': '',
            #'email': '',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title For Meeting:','required': True}),
            'date': forms.DateTimeInput(attrs={'class':'form-control','type': 'datetime-local', 'placeholder': 'Date and Time'}),
            'chair_meeting': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Chair OF The Meeting:','required': True}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            #'name': forms.TextInput(attrs={'class':'input', 'placeholder':'Your Name:'}),
            #'email': forms.EmailInput(attrs={'class':'input', 'placeholder':'Your Email:', 'required': True}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Purpose Of The Meeting',})
        }
        # help_texts = {
        #     'date': 'Please use the following format: <em>DD/MM/YYYY HH:MM</em>.',
        #             }
    def __init__(self, *args, **kwargs):
        super(TableMeetingForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:  # Only set default for new instances
            self.fields['date'].initial = timezone.now() 
            self.fields['title'].choices = [('HR', 'HR'), ('Finance', 'Finance'), ('IT', 'IT')]   

class AttendingForm(forms.ModelForm):
    class Meta:
        model = Attending
        fields = ['name','department','position','email']
        labels = {
            'name': '',
            'email': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'input', 'placeholder':'Your Name:'}),
            'department': forms.Select(attrs={'class': 'select'}),
            'position': forms.Select(attrs={'class': 'select'}),
            'email': forms.EmailInput(attrs={'class':'input', 'placeholder':'Your Email:', 'required': True})
        }
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            return name.upper()
        return name

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            return email.lower()
        return email
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Example choices for department and position
        self.fields['department'].widget.choices = [('HR', 'HR'), ('Finance', 'Finance'), ('IT', 'IT')]
        self.fields['position'].widget.choices = [('Manager', 'Manager'), ('Developer', 'Developer'), ('Analyst', 'Analyst')]


class MeetingForm(forms.ModelForm):
    class Meta:
        model = MeetingMinute
        fields = ['agenda','discussion','action_items_decisions', 'next_meeting_date']
        
        widgets = {
            'agenda': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'Agenda'}),
            'discussion': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'discussion'}),
            'action_items_decisions': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'Action Items/Decisions'}),
            'next_meeting_date': forms.DateTimeInput(attrs={'class': 'form-control','type': 'datetime-local', 'placeholder': 'Next Meeting Date'}),
        }
        help_texts = {
            'date': 'Please use the following format: <em>DD/MM/YYYY HH:MM</em>.',
        }
    def __init__(self, *args, **kwargs):
        super(MeetingForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:  # Only set default for new instances
            self.fields['next_meeting_date'].initial = timezone.now() 