from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from ..models.admin import ContactRequest ,TheAdmin
from ..models.talent import Talentee
from ..serialzers.ContactRequestSerializer import ContactRequestSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied


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
        user = request.user
        # Check if the logged-in user is an admin
        try:
            admin = TheAdmin.objects.get(user=user)
        except TheAdmin.DoesNotExist:
            raise PermissionDenied("You do not have permission to view this data.")
        # If the user is an admin, return all contact requests
        contact_requests = ContactRequest.objects.all()
        serializer = ContactRequestSerializer(contact_requests, many=True)
        return Response(serializer.data)
