# views.py
import re
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import TableMeeting, Attending, MeetingMinute
from .forms import TableMeetingForm, AttendingForm, MeetingForm
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404, HttpResponse, HttpResponseRedirect
import os
from PIL import Image
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from urllib.parse import unquote
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_GET


# def home(request):
#     error_message = request.GET.get('error', '')

#     if request.user.is_authenticated:
#         user_email = request.user.email.lower()
#         meetings = TableMeeting.objects.filter(attendees__email=user_email).distinct()
#     else:
#         meetings = []

#     return render(request, 'home.html', {'meetings': meetings, 'error_message': error_message})

# def join_meeting_page(request):
#     if request.method == 'GET':
#         meeting_link = request.GET.get('meeting_link')
        
#         if not meeting_link:
#             return JsonResponse({'error': 'Meeting link is required.'}, status=400)
        
#         try:
#             decoded_link = unquote(meeting_link)
#             match = re.search(r'/join_meeting/(\d+)/', decoded_link)
            
#             if match:
#                 meeting_id = match.group(1)
#                 return JsonResponse({'redirect_url': reverse('join_meeting', args=[meeting_id])})
#             else:
#                 return JsonResponse({'error': 'Invalid meeting link format.'}, status=400)
        
#         except Exception as e:
#             return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)
    
#     return redirect('home')
@csrf_protect
def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username').upper()
        email = request.POST.get('email').lower()
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!!")
        else:
            try:
                my_user = User.objects.create_user(uname, email, pass1)
                my_user.save()
                return redirect('meeting_view')
            except Exception as e:
                messages.error(request, 'Username or Password is incorrect!!!')
                return redirect('meeting_view') 
                #return HttpResponse(f"Error occurred: {str(e)}")

    return render(request, 'meeting_view.html')

@csrf_protect
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username').upper()
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            # Save user details to session
            request.session['user_email'] = user.email.lower()
            request.session['user_name'] = user.username.upper()
            messages.success(request, 'Login successful.')
            return redirect('meeting_view')
        else:
            messages.error(request, 'Username or Password is incorrect!!!')
            return redirect('meeting_view')  # Redirect to the login page to show the error message

    return render(request, 'meeting_view.html')

def LogoutPage(request):
    logout(request)
    return redirect('meeting_view')

@login_required(login_url='login')
def meeting_created(request, meeting_id):
    # Retrieve the meeting object using meeting_id
    meeting = get_object_or_404(TableMeeting, pk=meeting_id) 
    # Generate join URL
    join_url = reverse('join_meeting', args=[meeting_id])
    # Render the template with the meeting and join_url variables in the context
    return render(request, 'meeting_created.html', {'meeting': meeting, 'join_url': join_url})

@login_required(login_url='login')
def create_meeting(request, meeting_id=None):
    if meeting_id:
        meeting = get_object_or_404(TableMeeting, pk=meeting_id)
        is_edit = True
    else:
        meeting = None
        is_edit = False

    if request.method == 'POST':
        form = TableMeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            new_meeting = form.save(commit=False)
            new_meeting.email = request.session.get('user_email').lower()
            new_meeting.name = request.session.get('user_name').upper()
            new_meeting.save()
            if is_edit:
                messages.success(request, 'Meeting details updated successfully.')
                return redirect('meeting_details', meeting_id=form.instance.id)
            else:
                messages.success(request, 'Meeting created successfully.')
                return redirect('meeting_view')
    else:
        form = TableMeetingForm(instance=meeting)
        
    return render(request, 'create_meeting.html', {'form': form})

def join_meeting(request, meeting_id):
    meeting = get_object_or_404(TableMeeting, pk=meeting_id)
    form = AttendingForm(request.POST or None)

    if meeting.is_completed:
        messages.error(request, 'The meeting is completed and cannot be joined.')
        return redirect('meeting_view')

    if request.method == 'POST' and form.is_valid():
        name = form.cleaned_data['name'].upper()
        email = form.cleaned_data['email'].lower()
        attendee_exists = Attending.objects.filter(meeting=meeting, name=name, email=email).exists()

        if attendee_exists:
            messages.info(request, "You are already registered for this meeting.")
            return redirect('meeting_created' if (name == meeting.name and email == meeting.email) else 'meeting_list', meeting_id=meeting.id)

        # Create new attendee
        attendee = form.save(commit=False)
        attendee.meeting = meeting
        attendee.save()

        # Redirect based on the role
        if name == meeting.name and email == meeting.email:
            return redirect('meeting_created', meeting_id=meeting.id)
        else:
            return redirect('meeting_list', meeting_id=meeting.id)

    return render(request, 'join_meeting.html', {
        'meeting': meeting,
        'form': form,
    })
def meeting_view(request):
    meetings = TableMeeting.objects.order_by('-date')
    show_modal = request.session.pop('show_modal', False)
    modal_message = request.session.pop('modal_message', '')

    context = {
        'meetings': meetings,
        'show_modal': show_modal,
        'modal_message': modal_message,
    }

    return render(request, 'meeting_view.html', context)

def meeting_list(request, meeting_id):
    meeting = get_object_or_404(TableMeeting, pk=meeting_id)
    user_email = request.user.email.lower() if request.user.is_authenticated else None
    is_attendee = Attending.objects.filter(meeting=meeting, email=user_email).exists() if user_email else False
    pdf_exists = meeting.pdf_path and os.path.exists(meeting.pdf_path)
    can_generate_pdf = meeting.is_completed and (meeting.email.lower() == user_email or is_attendee)

    return render(request, 'meeting_list.html', {
        'meeting': meeting,
        'pdf_exists': pdf_exists,
        'can_generate_pdf': can_generate_pdf,
        'is_attendee': is_attendee
    })
@login_required(login_url='login')
def meeting_details(request, meeting_id):
    meeting = get_object_or_404(TableMeeting, pk=meeting_id)
    attendees = meeting.attendees.all()
    minutes = meeting.minutes.all()

    processed_minutes = []
    for minute in minutes:
        processed_minutes.append({
            'agenda': minute.agenda,
            'discussion': minute.discussion,
            'action_items_decisions': minute.action_items_decisions,
            'next_meeting_date': minute.next_meeting_date,
        })

    description_cleaned = meeting.description  # Assuming this is how you clean description

    # Initialize MeetingForm with instance of existing meeting
    meet = TableMeetingForm(instance=meeting)
    form = MeetingForm(instance=meeting)

    context = {
        'meeting': meeting,
        'attendees': attendees,
        'processed_minutes': processed_minutes,
        'description_cleaned': description_cleaned,
        'form': form, 
        'meet': meet, # Include form for editing meeting details
    }
    return render(request, 'meeting_details.html', context)

@login_required(login_url='login')
def add_minutes(request, meeting_id, minute_id=None):
    meeting = get_object_or_404(TableMeeting, pk=meeting_id)
    
    if minute_id:
        minute = get_object_or_404(MeetingMinute, pk=minute_id, table_meeting=meeting)
        is_edit = True
    else:
        # Check if minutes already exist for this meeting
        try:
            minute = MeetingMinute.objects.get(table_meeting=meeting)
            is_edit = True
        except MeetingMinute.DoesNotExist:
            minute = None
            is_edit = False

    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=minute)
        if form.is_valid():
            minute = form.save(commit=False)
            minute.table_meeting = meeting
            minute.save()

            if is_edit:
                messages.success(request, 'Meeting minutes updated successfully.')
            else:
                messages.success(request, 'Meeting minutes created successfully.')

            return redirect('meeting_details', meeting_id=meeting.id)  # Ensure this return statement is within the if block
    else:
        form = MeetingForm(instance=minute)

    return render(request, 'add_minutes.html', {'form': form, 'meeting': meeting, 'is_edit': is_edit})
def verify_attendee(request, attendee_id):
    attendee = get_object_or_404(Attending, pk=attendee_id)

    if request.method == 'POST':
        attendee.verified = True
        attendee.save()
        messages.success(request, f'{attendee.name} has been verified successfully.')
    
    return redirect('meeting_details', meeting_id=attendee.meeting.id)
@login_required(login_url='login')
def complete_meeting(request, meeting_id):
    meeting = get_object_or_404(TableMeeting, pk=meeting_id)

    if request.user.email.lower() != meeting.email.lower():
        messages.error(request, 'Only the meeting secretary can complete the meeting.')
        return redirect('meeting_details', meeting_id=meeting.id)  # Ensure correct redirection here

    if request.method == 'POST':
        try:
            meeting.is_completed = True
            meeting.save()
            messages.success(request, 'Meeting marked as completed.')
        except Exception as e:
            messages.error(request, f'Error completing meeting: {str(e)}')

        return redirect('meeting_details', meeting_id=meeting.id)  # Correct usage of redirect

    return render(request, 'complete_meeting.html', {'meeting': meeting})


def generate_pdf(request, meeting_id):
    try:
        meeting = get_object_or_404(TableMeeting, pk=meeting_id)
        attendees = meeting.attendees.filter(verified=True)
        minutes = meeting.minutes.all()

        if not meeting.is_completed:
            raise PermissionDenied('The meeting must be completed to generate the PDF.')

        # Check if the PDF already exists
        if meeting.pdf_path and os.path.exists(meeting.pdf_path):
            pdf_path = meeting.pdf_path
        else:
            processed_minutes = [
                {
                    'agenda': minute.agenda,
                    'discussion': minute.discussion,
                    'action_items_decisions': minute.action_items_decisions,
                    'next_meeting_date': minute.next_meeting_date,
                }
                for minute in minutes
            ]

            description_cleaned = meeting.description
            logo_path = os.path.join(settings.STATIC_URL, 'mymeeting/mymeeting/static/Asset 1NM.png')
            html_string = render_to_string('meeting_pdf.html', {
                'meeting': meeting,
                'attendees': attendees,
                'processed_minutes': processed_minutes,
                'description_cleaned': description_cleaned,
                'logo_path': logo_path,
            })

            html = HTML(string=html_string)
            pdf_path = os.path.join('pdfs', f'meeting_{meeting_id}.pdf')

            if not os.path.exists('pdfs'):
                os.makedirs('pdfs')

            html.write_pdf(target=pdf_path)
            meeting.pdf_path = pdf_path
            meeting.save()

        with open(pdf_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename=meeting_{meeting_id}.pdf'

        return response

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


def download_pdf(request, meeting_id):
    try:
        # Retrieve the meeting object
        meeting = get_object_or_404(TableMeeting, id=meeting_id)
        
        # Check if the user is authenticated and get their email
        user_email = request.user.email.lower() if request.user.is_authenticated else None

        # If user is not logged in, display an error
        if not user_email:
            messages.error(request, "You must be logged in to access this file.")
            return redirect('login')  # Redirect to login page

        # Check if the user is an attendee of the meeting
        is_attendee = Attending.objects.filter(meeting=meeting, email=user_email).exists()
        if not is_attendee:
            messages.error(request, "You do not have permission to access this file.")
            return redirect('meeting_view', meeting_id=meeting_id)  # Redirect to meeting view page

        # Verify if the PDF path exists
        pdf_path = meeting.pdf_path
        if not pdf_path or not os.path.exists(pdf_path):
            messages.error(request, "PDF file not found.")
            return redirect('meeting_details', meeting_id=meeting_id)  # Redirect to meeting details page

        # Serve the PDF file
        response = FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'
        return response

    except PermissionDenied as e:
        # Handle permission errors
        messages.error(request, f"Permission denied: {str(e)}")
        return redirect('meeting_view', meeting_id=meeting_id)

    except FileNotFoundError:
        # Handle file not found errors
        messages.error(request, "PDF file not found.")
        return redirect('meeting_details', meeting_id=meeting_id)

    except Exception as e:
        # Handle other unexpected errors
        #messages.error(request, f"An unexpected error occurred: {str(e)}")
        return redirect('meeting_view')  # Redirect to a safe page