
from ..serialzers.SkillSerializer import SkillSerlaizer
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models.Skill import Skill


class SkillView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        skills=Skill.objects.all()
        print(request.data)
        
        data = SkillSerlaizer(skills, many=True).data
        return Response(data)
    
    
