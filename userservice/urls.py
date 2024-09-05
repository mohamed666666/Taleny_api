from rest_framework_simplejwt.views import TokenObtainPairView ,TokenRefreshView
from django.urls import path 
from .views.TalenteeViews import TalenteeRegistrationView


app_name ='userservice'
urlpatterns = [
    path("token/",TokenObtainPairView.as_view(),name="token"),#get token by username and password 
    path("token/refresh/",TokenRefreshView.as_view(),name="refresh"),
    
    #Talentee
    path('register/Talentee/', TalenteeRegistrationView.as_view(), name='register-Talentee'),
]