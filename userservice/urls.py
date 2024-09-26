from rest_framework_simplejwt.views import  TokenRefreshView
from django.urls import path 
from .views.TalenteeViews import TalenteeRegistrationView
from .views.TalentView import TalentView
from .views.InvestgatorViews import InvestgatorRegistrationView
from .views.LoginView import CustomTokenObtainPairView
from .views.SkillViews import CreateSkillView,TalnenteeSkillsView,TalnenteeSkillsViewByID
from .views.FollowViews import (FollowCreateView,FollowDeleteView,FollowersToCurrentUserView,
                               AcceptFollowView,usersFollowedByCurrentUserView )
from .views.InterstsViews import (Get_allInterstsView,SelectInterestView,
                                 GetCurrentUserInterestsView  ,GetUserInterestsByIDView)
from .views.AdminViews import ContactRequestCreateView,ContactRequestListView
from .views.Usersviews import UsersOrderByInterstsView
from .views.ProfileViews import UserProflieByid,UpdateUserProflie

from django.conf import settings
from django.conf.urls.static import static


app_name ='userservice'
urlpatterns = [
    path("login/",CustomTokenObtainPairView.as_view(),name="login"),#get token by username and password 
    path("token/refresh/",TokenRefreshView.as_view(),name="refresh"),
    #adimn 
    path('contactrequest/<int:talentee_id>/', ContactRequestCreateView.as_view(), name='create-contact-request'),
    path('contactrequests/', ContactRequestListView.as_view(), name='get-all-contact-requests-for-admin'),
    
    #Talentee
    path('register/Talentee/', TalenteeRegistrationView.as_view(), name='register-Talentee'),
    #talent views
    path('all_talents/',TalentView.as_view(),name='get_all_talents') ,
    #investgator
    path('register/Investgator/', InvestgatorRegistrationView.as_view(), name='register-Investgator'),
    # skill crud
    path('addskill/',CreateSkillView.as_view(),name='add_skill'),
    path('talenteeskills/',TalnenteeSkillsView.as_view(),name='get_skills'),
    path('talenteeskills/<int:user_id>/',TalnenteeSkillsViewByID.as_view(),name='get_skills_byid'),
    
    
    
    # follow crud
    path('createfollow/',FollowCreateView.as_view(),name='create_follow'),
    path('deletefollow/',FollowDeleteView.as_view(),name='delete_follow'),
    path('followers/',FollowersToCurrentUserView.as_view(),name='get_follows_current_user'),
    path('accept_follow/',AcceptFollowView.as_view(),name='accept_follows_current_user'),
    path('following/',usersFollowedByCurrentUserView.as_view(),name='get_follows_of_current_user'),
    #user profile  
    path('user_profile/<int:user_id>/',UserProflieByid.as_view(),name='get_user_data_by_id'),
    path('user_profile/update/',UpdateUserProflie.as_view(),name='get_user_data_by_id'),
    
    # intersts 
    path('all_intersts/',Get_allInterstsView.as_view(),name='get_all_intersts'),
    path('selectInterst/',SelectInterestView.as_view(),name='select_interst_by_id'),
    path('currentuserintersts/',GetCurrentUserInterestsView.as_view(),name='select_currentuserintersts'),
    path('userintersts/<int:user_id>/',GetUserInterestsByIDView.as_view(),name='select_userintersts'),
    path('sugested-users/',UsersOrderByInterstsView.as_view(),name='get_users_with_common_interst')
]