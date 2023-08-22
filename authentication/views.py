from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class UserDetailsView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self, request, *args, **kwargs):
    user = User.objects.get(id=request.user.id)
    serializer = UserSerializer(instance=user)
    return Response(serializer.data, status=status.HTTP_200_OK)


