from django.urls import path
from .views.LikeViews import LikeCreateView ,LikeDeleteView
from .views.PostViews import CreatePostView
app_name ='blogservice'
urlpatterns = [
    path('like/', LikeCreateView.as_view(), name='like-create'),
    path('like/delete/', LikeDeleteView.as_view(), name='like-delete'),
    
     path('create-post/', CreatePostView.as_view(), name='create-post'),
]