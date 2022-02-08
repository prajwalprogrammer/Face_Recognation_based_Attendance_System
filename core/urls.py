import profile
from django.urls import path
from core.views import SignUpView, ProfileView,HomePageView,AboutPageView,ProfileView1
from .views import *

urlpatterns = [
    # path('', HomePageView.as_view(), name='homepage'),
    path('add/', add_profile, name='addprofile'),
    path('about/', about, name='about'),
    path('signup/', register, name='signup'),
    path('MarkAttendance/', TrackImages, name='markAttendace'),
    path('TakeImage/', TakeImage, name='TakeImage'),
    # path('TrainImage/', TrainImages, name='TrainImages'),
    path('desplayAttendance/', desplayAttendance, name='desplayAttendance'),
    path('sendmail/', send_email, name='sendmail'),

    path('profile/', profile, name='pdata'),
    path('GenerateCode/', GenerateCode, name='GenerateCode'),
    # path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),



    path('profile/<int:id>/', edit_profile, name='profile'),
]