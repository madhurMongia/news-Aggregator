from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from .models import newUser
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.conf import settings
from django.utils import timezone
from rest_framework.authtoken.models import Token
from .serilizers import UserSerializer,newTokenSerializer
from urllib.parse import urlparse
class RegistionView(APIView):

    def post(self, request):
        serilizer = UserSerializer(data= request.data)
        if serilizer.is_valid():
            account = serilizer.save()
            user_name = serilizer.validated_data['user_name']
            token = Token.objects.create(user = account)
            uri = request.build_absolute_uri()
            send_verification_email_task.delay(
                user_name, token.key, account.email, uri)
            return Response({'msg': "user with username " + user_name + " created "}, status=status.HTTP_201_CREATED)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self,request):
        serializer = newTokenSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = get_object_or_404(
                Token, user=serializer.validated_data['user'])
            user.last_login = timezone.now()
            user.save()
            return Response({'key' : token.key},status = status.HTTP_200_OK)
        return Response(serializer.errors,status =status.HTTP_400_BAD_REQUEST)


class VerificationView(APIView):
    def get(self, request, token):
        user = get_object_or_404(newUser, auth_token__key=token)
        user.is_active = True
        user.save()
        return Response({'msg': 'user verified'}, status=status.HTTP_200_OK)


@shared_task
def send_verification_email_task(username, key, email, uri):
    url = urlparse(uri)
    email = EmailMessage(subject='Email Verification',
                         body=f'{url.scheme}://{url.netloc}/user/verify/{key}',
                         from_email=settings.EMAIL_HOST_USER, to=[email])

    return email.send(fail_silently=False)
