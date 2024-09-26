from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated 

from ..models.Post import Post ,Post_attachement
from ..models.Like import Like
from ..models.Comment import Comment
from django.contrib.contenttypes.models import ContentType
from ..Serializers.LikeSerializer import LikeSerializer

from ..Serializers.PostSerializer import PostSerializer ,RetrivePostSerializer
from ..Serializers.PostSerializer import PostAttachmentSerializer
from userservice.serialzers.BaseUserSerlaizer import UserSerializer



