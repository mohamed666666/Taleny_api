
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from ..models.Baseuser import UserBase
from ..models.inetrsts import Intersting_in
from ..serialzers.BaseUserSerlaizer import UserSerializer


class UsersOrderByInterstsView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        # Step 1: Get the interests of the logged-in user
        user_interests = Intersting_in.objects.filter(user=request.user).values_list('interst', flat=True)
        # Step 2: Get all users and annotate with shared_interests count (including 0 for no shared interests)
        users_with_shared_interests = (
            UserBase.objects
            .exclude(id=request.user.id)  # Exclude the request.user
            .annotate(
                shared_interests=Count('intersting_in__interst', filter=Q(intersting_in__interst__in=user_interests))
            )
            .order_by('-shared_interests')  # Order by number of shared interests
        )

        # Step 3: Serialize the data
        serializer = UserSerializer(users_with_shared_interests, many=True)

        # Step 4: Return the response
        return Response(serializer.data)