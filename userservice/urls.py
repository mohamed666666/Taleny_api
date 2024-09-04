from rest_framework_simplejwt.views import TokenObtainPairView ,TokenRefreshView
from django.urls import path 


app_name ='userservice'
urlpatterns = [
    path("token/",TokenObtainPairView.as_view(),name="token"),#get token by username and password 
    path("token/refresh/",TokenRefreshView.as_view(),name="refresh"),
]