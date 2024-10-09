
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from ..models.Baseuser import UserBase
from ..models.inetrsts import Intersting_in
from ..serialzers.BaseUserSerlaizer import UserSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework import status
    

class UsersOrderByInterstsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Step 1: Get the interests of the logged-in user
        user_interests = Intersting_in.objects.filter(user=request.user).values_list('interst', flat=True)
        
        # Step 2: Get all users (excluding Admins) and annotate with shared_interests count
        users_with_shared_interests = (
            UserBase.objects
            .exclude(id=request.user.id)  # Exclude the request.user
            .filter(Q(talentee__isnull=False) | Q(investgator__isnull=False))  # Exclude Admins
            .annotate(
                shared_interests=Count('intersting_in__interst', filter=Q(intersting_in__interst__in=user_interests))
            )
            .order_by('-shared_interests')  # Order by number of shared interests
        )

        # Step 3: Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 30  # You can adjust the page size here
        paginated_users = paginator.paginate_queryset(users_with_shared_interests, request)

        # Step 4: Serialize the paginated data
        serializer = UserSerializer(paginated_users, many=True)
        
        # Step 5: Return paginated response
        return paginator.get_paginated_response(serializer.data)




class UserSearchAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', None)
        
        # Search logic
        if query:
            users = UserBase.objects.filter(
                Q(user_name__icontains=query) | 
                Q(full_name__icontains=query) |
                Q(title__icontains=query)   
                
            ).exclude(Q(theadmin__isnull=False))
           
        else:
            users = UserBase.objects.all().exclude(Q(theadmin__isnull=False))

        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 30  # Set page size before paginate_queryset
        paginated_users = paginator.paginate_queryset(users, request)

        # Serialize and return paginated data
        serializer = self.get_serializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)
