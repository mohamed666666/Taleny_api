from rest_framework.response import Response
from rest_framework import status
from ..models.Baseuser import UserBase
from ..models.inetrsts import Interst,Intersting_in
from ..serialzers.InterestSerializer import InterstSerlaizer
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class Get_allInterstsView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request):
        obs = Interst.objects.all()  # Queryset of all Interst objects
        serializer = InterstSerlaizer(obs, many=True)  # No 'data' argument needed here
        return Response(serializer.data)
        
        
class SelectInterestView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user  # Get the authenticated user
        interest_id = request.data.get('interest_id')  # Get the interest ID from the request
        
        try:
            # Fetch the interest from the database using the provided ID
            interest = Interst.objects.get(id=interest_id)
            # Create the Intersting_in object to link the user and the interest
            
            if (Intersting_in.objects.filter(user=user, interst=interest).exists()):
                return Response({'message': 'you already select this interest'}, status=405)
            intersting_in = Intersting_in.objects.create(user=user, interst=interest)
            intersting_in.save()
            return Response({'message': 'Interest selected successfully!'}, status=201)
        except Interst.DoesNotExist:
            return Response({'error': 'Interest not found!'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
        
    def delete(self,request):
        user = request.user  # Get the authenticated user
        interest_id = request.data.get('interest_id')
        interst=get_object_or_404(Interst,id=interest_id)
        intersting_in=Intersting_in.objects.filter(user=user,interst=interst)
        intersting_in.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    
        
        
        
class GetCurrentUserInterestsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user  # Get the authenticated user
        # Get all Intersting_in objects related to this user
        user_interests = Intersting_in.objects.filter(user=user)
        # Extract the 'interst' field from each Intersting_in object
        interests = [item.interst for item in user_interests]
        # Serialize the list of Interst objects
        serializer = InterstSerlaizer(interests, many=True)
        return Response(serializer.data, status=200)





class GetUserInterestsByIDView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request ,user_id):
        user = UserBase.objects.get(id=user_id)
        # Get all Intersting_in objects related to this user
        user_interests = Intersting_in.objects.filter(user=user)
        # Extract the 'interst' field from each Intersting_in object
        interests = [item.interst for item in user_interests]
        # Serialize the list of Interst objects
        serializer = InterstSerlaizer(interests, many=True)
        
        return Response(serializer.data, status=200)
    
    
