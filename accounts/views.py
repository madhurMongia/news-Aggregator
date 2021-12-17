from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from .models import newUser
from django.utils import timezone
from rest_framework.authtoken.models import Token
from .serilizers import UserSerializer,newTokenSerializer
class RegistionView(APIView):

    def post(self, request):
        serilizer = UserSerializer(data= request.data)
        if serilizer.is_valid():
            account = serilizer.save()
            user_name = serilizer.validated_data['user_name']
            token = Token.objects.create(user = account)
            return Response({ 'msg' : "user with username " + user_name + " created ", 'key' : token.key},status = status.HTTP_201_CREATED)
        return Response(serilizer.errors,status =status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):

    def post(self,request):
        serializer = newTokenSerializer(data = request.data)

        if serializer.is_valid():
            token = get_object_or_404(Token,user =serializer.validated_data['user'])
            user = newUser.objects.get(email = serializer.validated_data['email'])
            user.last_login = timezone.now()
            user.save()
            return Response({'key' : token.key},status = status.HTTP_200_OK)
        return Response(serializer.errors,status =status.HTTP_400_BAD_REQUEST)

