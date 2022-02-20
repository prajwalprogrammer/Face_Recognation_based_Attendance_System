import profile
from django.urls import path
from core.views import SignUpView, ProfileView,HomePageView,AboutPageView,ProfileView1
from .views import *

urlpatterns = [
    path('about/', about, name='about'),
    path('MarkAttendance/', TrackImages, name='markAttendace'),
    path('TakeImage/', TakeImage, name='TakeImage'),
    path('desplayAttendance/', desplayAttendance, name='desplayAttendance'),
    path('sendmail/', send_email, name='sendmail'),
    path('profile/', profile, name='pdata'),
    path('profile/<int:id>/', edit_profile, name='profile'),
]