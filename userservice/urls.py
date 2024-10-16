from rest_framework_simplejwt.views import  TokenRefreshView
from django.urls import path 
from .views.TalenteeViews import TalenteeRegistrationView
from .views.TalentView import TalentView
from .views.InvestgatorViews import InvestgatorRegistrationView
from .views.LoginView import CustomTokenObtainPairView

#skill 
from .views.SkillViews import (SkillCreateGetView,
                               TalnenteeSkillsViewByID,
                               UpdateSkillView,
                               DeleteSkillView,
                               SkillByID)
#follow viwes 
from .views.FollowViews import (FollowCreateView,
                                FollowDeleteView,FollowersToCurrentUserView,
                               AcceptFollowView,usersFollowedByCurrentUserView ,
                               FollowerRequestsToCurrentUserView,FollowRejectView
                               )
#inersts 
from .views.InterstsViews import (Get_allInterstsView,SelectInterestView,
                                 GetCurrentUserInterestsView  ,GetUserInterestsByIDView)

from .views.AdminViews import (ContactRequestCreateView,GetTalenteeByIdViews,
                               ContactRequestListView,GetInvestByIdViews,
                               GetAllTalenteesViews, GetAllInvestsViews,
                               ContactRequestByidView,StatsticsForAdminView,
                               ContactRequestHistoryView
                               )
from .views.Usersviews import (UsersOrderByInterstsView, 
                               UserSearchAPIView
)
from .views.ProfileViews import( UserProflieByid,CurrentUserProflie,
                                UpdateUserProflie , UserProflieStastics,
                                CurrentUserProflieStastics
                                )

from django.conf import settings
from django.conf.urls.static import static


app_name ='userservice'
urlpatterns = [
    path("login/",CustomTokenObtainPairView.as_view(),name="login"),#get token by username and password 
    path("token/refresh/",TokenRefreshView.as_view(),name="refresh"),
    
    #adimn 
    path('contactrequest/<int:talentee_id>/', ContactRequestCreateView.as_view(), name='create-contact-request'),
    path('contactrequests/', ContactRequestListView.as_view(), name='get-all-contact-requests-for-admin'),
    path('contactrequests/<int:request_id>/', ContactRequestByidView.as_view(), name='get-by-id-contact-request'),
    path('all_telentees/', GetAllTalenteesViews.as_view(), name='get-all-talentees-for-admin'),
    path('all_investgators/', GetAllInvestsViews.as_view(), name='get-all-investgators-for-admin'),
    path('telentee/<int:user_id>/', GetTalenteeByIdViews.as_view(), name='get-talentee-by-id-admin-for-admin'),
    path('Investgator/<int:user_id>/', GetInvestByIdViews.as_view(), name='get-Investgator-by-id-for-admin'),
    path('stastics/admin/', StatsticsForAdminView.as_view(), name='numbers-(t,i,c)-for-admin'),
    path('contactrequests/history/<int:year>/', ContactRequestHistoryView.as_view(), name='contact-request-history'),
    #Talentee
    path('register/Talentee/', TalenteeRegistrationView.as_view(), name='register-Talentee'),
    #talent views
    path('all_talents/',TalentView.as_view(),name='get_all_talents') ,
    #investgator
    path('register/Investgator/', InvestgatorRegistrationView.as_view(), name='register-Investgator'),
    # skill crud
    path('talenteeskills/',SkillCreateGetView.as_view(),name='add_skill'),
    path('talenteeskills/',SkillCreateGetView.as_view(),name='get_skills'),
    path('talentee-skill/<int:skill_id>/',SkillByID.as_view(),name='get_skill_by_skill-id'),
    path('talenteeskills/<str:user_name>/',TalnenteeSkillsViewByID.as_view(),name='get_skills_byusr-id'),
    path('talenteeskills/update/<int:skill_id>/',UpdateSkillView.as_view(),name='update_skilldata_by-skill-id'),
    path('talenteeskills/delete/<int:skill_id>/',DeleteSkillView.as_view(),name='delete_skilldata_by-skill-id'),
    
    
    
    # follow crud
    path('createfollow/',FollowCreateView.as_view(),name='create_follow'),
    path('deletefollow/',FollowDeleteView.as_view(),name='delete_follow'),
    path('follow_requests/',FollowerRequestsToCurrentUserView.as_view(),name='get_pending_requests'),
    path('followers/',FollowersToCurrentUserView.as_view(),name='get_followers_to_current_user'),
    path('accept_follow/',AcceptFollowView.as_view(),name='accept_follows_current_user'),
    path('reject_follow/<int:follow_id>/',FollowRejectView.as_view(),name='reject_follows_current_user'),
    path('following/',usersFollowedByCurrentUserView.as_view(),name='get_followings_of_current_user'),
    
    #user profile  
    path('user_profile/', CurrentUserProflie.as_view(), name='current_user_data'),
    path('user_profile/<str:user_name>/',UserProflieByid.as_view(),name='get_user_data_by_username'),
    path('user_profile/update/<str:user_name>/',UpdateUserProflie.as_view(),name='update_user_data-by-username'),
    path('profile/statstics/', CurrentUserProflieStastics.as_view(), name='statsics-of-Current-user'),
    path('profile/statstics/<str:user_name>/', UserProflieStastics.as_view(), name='statsics-of-user-by-user_name'),
    
    #search for users 
    
    path('search/',UserSearchAPIView.as_view(),name='serach_by_q parameter_get_user_data'),
    
    # intersts 
    path('all_intersts/',Get_allInterstsView.as_view(),name='get_all_intersts'),
    path('selectInterst/',SelectInterestView.as_view(),name='select_interst_by_id'),
    path('currentuserintersts/',GetCurrentUserInterestsView.as_view(),name='select_currentuserintersts'),
    path('userintersts/<int:user_id>/',GetUserInterestsByIDView.as_view(),name='select_userintersts'),
    path('sugested-users/',UsersOrderByInterstsView.as_view(),name='get_users_with_common_interst')
]