from rest_framework_simplejwt.views import  TokenRefreshView
from django.urls import path 
from .views.TalenteeViews import TalenteeRegistrationView
from .views.TalentView import TalentView
from .views.InvestgatorViews import InvestgatorRegistrationView
from .views.LoginView import CustomTokenObtainPairView
app_name ='userservice'
urlpatterns = [
    path("login/",CustomTokenObtainPairView.as_view(),name="login"),#get token by username and password 
    path("token/refresh/",TokenRefreshView.as_view(),name="refresh"),
    
    #Talentee
    path('register/Talentee/', TalenteeRegistrationView.as_view(), name='register-Talentee'),
    #talent views
    path('alltalents',TalentView.as_view(),name='all_talents')
    ,
    #investgator
     path('register/Investgator/', InvestgatorRegistrationView.as_view(), name='register-Investgator'),
]