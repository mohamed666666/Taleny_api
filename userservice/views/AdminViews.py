from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from ..models.admin import ContactRequest ,TheAdmin
from ..models.talent import Talentee
from ..models.investgator import Investgator
from ..serialzers.ContactRequestSerializer import ContactRequestSerializer
from ..serialzers.TalenteeSerializer import TalenteeRetriveSerializer
from ..serialzers.InvestgatorSerlaizer import InvestgatorRetriveSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


class ContactRequestCreateView(generics.CreateAPIView):
    serializer_class = ContactRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        talentee_id = self.kwargs['talentee_id']
        
        try:
            talentee = Talentee.objects.get(pk=talentee_id)
        except Talentee.DoesNotExist:
            raise ValidationError({"detail": "Talentee does not exist."})

        # Ensure that an Investigator can only request a Talentee once
        request_creator = self.request.user.investgator
        if ContactRequest.objects.filter(request_creator=request_creator, talentee_requested=talentee).exists():
            raise ValidationError({"detail": "You have already sent a contact request to this Talentee."})
        
        serializer.save(talentee_requested=talentee)
        
        return Response(status=status.HTTP_201_CREATED)
        
        

class ContactRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        adminpermssion(request.user)
        # If the user is an admin, return all contact requests
        contact_requests = ContactRequest.objects.all()
        serializer = ContactRequestSerializer(contact_requests, many=True)
        return Response(serializer.data)


class ContactRequestByidView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,request_id):
        adminpermssion(request.user)
        # If the user is an admin, return all contact requests
        contact_request = ContactRequest.objects.get(pk=request_id)
        serializer = ContactRequestSerializer(contact_request)
        return Response(serializer.data)



class StatsticsForAdminView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        adminpermssion(request.user)
        taltentees=Talentee.objects.all().count()
        invetsgators=Investgator.objects.all().count()
        contact_requests=ContactRequest.objects.all().count()
        return Response ({'Talentees_count':taltentees,
                          'Investgators_count':invetsgators,
                          'Contact_Requests_count':contact_requests} ,status=200)


class GetAllTalenteesViews(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        adminpermssion(request.user)
        talentees=Talentee.objects.all()
        serializer=TalenteeRetriveSerializer(talentees,many=True)
        return Response(serializer.data,status=200)
    

class GetTalenteeByIdViews(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,user_id):
        adminpermssion(request.user)
        talentee=get_object_or_404(Talentee,pk=user_id)
        serializer=TalenteeRetriveSerializer(talentee)
        return Response(serializer.data,status=200)
    
    
class GetAllInvestsViews(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        adminpermssion(request.user)
        invests=Investgator.objects.all()
        serializer=InvestgatorRetriveSerializer(invests,many=True)
        return Response(serializer.data,status=200)
    
class GetInvestByIdViews(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,user_id):
        adminpermssion(request.user)
        invest=get_object_or_404(Investgator,pk=user_id)
        serializer=InvestgatorRetriveSerializer(invest)
        return Response(serializer.data,status=200)

    
    
def adminpermssion(user):
        try:
            admin = TheAdmin.objects.get(user=user)
        except TheAdmin.DoesNotExist:
            raise PermissionDenied("You do not have permission to view this data.")