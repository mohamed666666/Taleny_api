from django.urls import path
from .views.LikeViews import LikeCreateView ,LikeDeleteView
from .views.PostViews import CreatePostView,RetrivePost_by_id,UpdatePostView,DeletePost_by_id

from .views.CommentViews import  (
    CommentRetrieveByIdView,CommentRetrieveByPostIdView, 
    CommentCreateView,CommentUpdateView,CommentDeleteView,)


app_name ='blogservice'
urlpatterns = [
    path('like/', LikeCreateView.as_view(), name='like-create'),
    path('like/delete/', LikeDeleteView.as_view(), name='like-delete'),
    #post crud
    path('create-post/', CreatePostView.as_view(), name='create-post'),
    path('get-post/<int:post_id>/', RetrivePost_by_id.as_view(), name='get-post-by-id'),
    path('update-post/<int:post_id>/', UpdatePostView.as_view(), name='Update-post-by-id'),
    path('delete-post/<int:post_id>/', DeletePost_by_id.as_view(), name='delete-post-by-id'),
    # Comment crud 
    path('comments/<int:comment_id>/', CommentRetrieveByIdView.as_view(), name='comment-detail'),
    path('comments/post/<int:post_id>/', CommentRetrieveByPostIdView.as_view(), name='comments-by-post'),
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/update/<int:comment_id>/', CommentUpdateView.as_view(), name='comment-update'),
    path('comments/delete/<int:comment_id>/', CommentDeleteView.as_view(), name='comment-delete'),
    
]