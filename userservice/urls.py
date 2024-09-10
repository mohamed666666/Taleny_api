from rest_framework_simplejwt.views import  TokenRefreshView
from django.urls import path 
from .views.TalenteeViews import TalenteeRegistrationView
from .views.TalentView import TalentView
from .views.InvestgatorViews import InvestgatorRegistrationView
from .views.LoginView import CustomTokenObtainPairView
from .views.SkillViews import CreateSkillView,TalnenteeSkillsView,TalnenteeByIDSkillsView
from .views.FollowViews import FollowCreateView,FollowDeleteView,UserFollowersView

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
    # skill crud
    path('addskill/',CreateSkillView.as_view(),name='add_skill'),
    path('talenteeskills/',TalnenteeSkillsView.as_view(),name='get_skills'),
    path('talenteeskills/<int:user_id>/',TalnenteeByIDSkillsView.as_view(),name='get_skills_byid'),
    # follow crud
    path('createfollow/',FollowCreateView.as_view(),name='create_follow'),
    path('deletefollow/',FollowDeleteView.as_view(),name='delete_follow'),
    path('follows_to_user/',UserFollowersView.as_view(),name='follows_to_user')
    
]