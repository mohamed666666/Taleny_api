from django.urls import path
from .views.LikeViews import( LikeCreateAPIView ,LikeDeleteAPIView,
                             GetLikesOnPost,GetLikesOnComment
                             )
from .views.PostViews import (CreatePostView,RetrivePost_by_id,
                              UpdatePostView,DeletePost_by_id,
                              GetAllPostsView,GetPostsOfCurrentUserView,
                              GetPostsOfUserByIdView
                              )

from .views.CommentViews import  (
                                CommentRetrieveByIdView,CommentRetrieveByPostIdView, 
                                CommentCreateView,CommentUpdateView,
                                CommentDeleteView,)

from .views.ShareViews import (ShareListCreateAPIView ,
                               ShareDetailAPIView,
                               ShareListOfUserByUsernameView
                                )


app_name ='blogservice'
urlpatterns = [
    path('like/', LikeCreateAPIView.as_view(), name='like-create'),
    path('like/delete/', LikeDeleteAPIView.as_view(), name='like-delete'),
    path('like/post/<int:post_id>/', GetLikesOnPost.as_view(), name='get-likes-on-post-by-post_id'),
    path('like/comment/<int:comment_id>/', GetLikesOnComment.as_view(), name='get-likes-on-comment-by-comment_id'),
    
    #post crud
    path('create-post/', CreatePostView.as_view(), name='create-post'),
    path('get-post/<int:post_id>/', RetrivePost_by_id.as_view(), name='get-post-by-id'),
    path('update-post/<int:post_id>/', UpdatePostView.as_view(), name='Update-post-by-id'),
    path('delete-post/<int:post_id>/', DeletePost_by_id.as_view(), name='delete-post-by-id'),
    path('feed/', GetAllPostsView.as_view(), name='get-all-posts'),
    path('user-posts/', GetPostsOfCurrentUserView.as_view(), name='get-posts-of-current-user'),
    path('user-posts/<str:user_name>/', GetPostsOfUserByIdView.as_view(), name='get-posts-of-user-by_user-name'),
    #shares 
    path('share/', ShareListCreateAPIView.as_view(), name='get-shares-of-current-user-and-create-share'),
    path('share/<int:share_id>/', ShareDetailAPIView.as_view(), name='get-shares-and-delete-share-by-share_id'),
    path('shares/<str:user_name>/', ShareListOfUserByUsernameView.as_view(), name='get-shares-of-user-by_user-name'),
    
    
    # Comment crud 
    path('comments/<int:comment_id>/', CommentRetrieveByIdView.as_view(), name='comment-detail'),
    path('comments/post/<int:post_id>/', CommentRetrieveByPostIdView.as_view(), name='comments-on-post-by-postid'),
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/update/<int:comment_id>/', CommentUpdateView.as_view(), name='comment-update'),
    path('comments/delete/<int:comment_id>/', CommentDeleteView.as_view(), name='comment-delete'),
    
    
]