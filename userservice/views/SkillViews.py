from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.Skill import skilled_in,Skill_attachments,Skill
from django.shortcuts import get_object_or_404
from ..models.talent import Talentee
from ..serialzers.SkillSerializer import SkillSerializer,SkillAttachmentsSerializer,SkilledInSerializer
from rest_framework.parsers import MultiPartParser, FormParser



class SkillCreateGetView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        # Get the authenticated user and find their Talentee profile
        user = request.user
        talentee = get_object_or_404(Talentee, user=user)
        
        # Extract skill data from the request
        skill_data = {
            'name': request.data.get('skill.name'),
            'skill_desc': request.data.get('skill.skill_desc')
        }
        attachments = request.FILES.getlist('attachments') 
        # Get list of files from request
     
        skill_serializer = SkillSerializer(data=skill_data)
        if skill_serializer.is_valid():
            # Save the skill instance
            skill = skill_serializer.save()
            # Create a skilled_in object to link Talentee and Skill
            skilled_in.objects.create(talentee=talentee, skill=skill)
            # Link the created skill with attachments
            for file in attachments:
                Skill_attachments.objects.create(skill=skill, uri=file)
            # Create a response with the created skill and its attachments
            skill_with_attachments = {
                "skill": skill_serializer.data,
                "attachments": SkillAttachmentsSerializer(skill.skill_attachments_set.all(), many=True).data
            }
            return Response(skill_with_attachments, status=status.HTTP_201_CREATED)
        return Response(skill_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        # Get the authenticated user and find their Talentee profile
        user = request.user
        talentee = get_object_or_404(Talentee, user=user)
        # Retrieve all skills linked to the Talentee via the skilled_in model
        skilled_at = skilled_in.objects.filter(talentee=talentee)
        # Serialize the skilled_in instances with related skills and attachments
        serializer = SkilledInSerializer(skilled_at, many=True)
        return Response(serializer.data)



class UpdateSkillView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    parser_classes = [MultiPartParser, FormParser]
    
    def put(self, request,skill_id):
        # Get the authenticated user and find their Talentee profile
        user = request.user
        talentee = get_object_or_404(Talentee, user=user)
        # Fetch the skill instance
        skill = get_object_or_404(Skill, id=skill_id)
        # Extract skill data from the request
        attachments = request.FILES.getlist('attachments')  # Get list of files from request
        serializer = SkillSerializer(skill, data=request.data, partial=True)
        if serializer.is_valid():
            # Use serializer's update method
            serializer.update(skill, validated_data=serializer.validated_data)
            return Response(serializer.data, status=200)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteSkillView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self,request,skill_id):
        talentee= get_object_or_404(Talentee, user=request.user)
        skill = get_object_or_404(Skill, id=skill_id)
        skill.delete()
        return Response(status=200)
        




    
    

class TalnenteeSkillsViewByID(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        # Find the Talentee profile by the provided user ID
        talentee = get_object_or_404(Talentee, user__id=user_id)
        # Retrieve all skills linked to the Talentee via the skilled_in model
        skilled_at = skilled_in.objects.filter(talentee=talentee)
        # Serialize the skilled_in instances with related skills and attachments
        serializer = SkilledInSerializer(skilled_at, many=True)
        return Response(serializer.data)
    
    
class SkillByID(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, skill_id):
        user = request.user
        talentee = get_object_or_404(Talentee, user=user)
        # Retrieve all skills linked to the Talentee via the skilled_in model
        skill = get_object_or_404(Skill, id=skill_id)
        skilled_at = skilled_in.objects.filter(talentee=talentee, skill=skill)
       
        
        # Serialize the skilled_in instances with related skills and attachments
        serializer = SkilledInSerializer(skilled_at, many=True)  # many=True to handle a QuerySet
        return Response(serializer.data)