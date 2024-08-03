# urls.py
from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.meeting_view, name='meeting_view'),
    path('singnup/',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('logout/',views.LogoutPage,name='logout'),
    path('complete_meeting/<int:meeting_id>/', views.complete_meeting, name='complete_meeting'),
    path('meeting_view', views.meeting_view, name='meeting_view'),
    path('create_meeting/', views.create_meeting, name='create_meeting'),
    path('join_meeting/<int:meeting_id>/', views.join_meeting, name='join_meeting'),
     path('verify_attendee/<int:attendee_id>/', views.verify_attendee, name='verify_attendee'),
    # path('join_meeting_page/', views.join_meeting_page, name='join_meeting_page'),
    path('add_minutes/<int:meeting_id>/', views.add_minutes, name='add_minutes'),
    path('generate_pdf/<int:meeting_id>/', views.generate_pdf, name='generate_pdf'),
    # path('generate2_pdf/<int:meeting_id>/', views.generate2_pdf, name='generate2_pdf'),
    path('meeting_details/<int:meeting_id>/', views.meeting_details, name='meeting_details'),
    path('meeting_created/<int:meeting_id>/', views.meeting_created, name='meeting_created'),
    path('edit_minutes/<int:meeting_id>/<int:minute_id>/', views.add_minutes, name='edit_minutes'),
    path('meeting_list/<int:meeting_id>/', views.meeting_list, name='meeting_list'),
    path('create_meeting/<int:meeting_id>/', views.create_meeting, name='create_meeting'),
    path('download_pdf/<int:meeting_id>/', views.download_pdf, name='download_pdf'),
]
    

