# import rest frame work modules here

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, views

# ipmort django modules here

from django.contrib.auth import logout
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator

# import modules from project and apps here

from MicroService import settings
from Accounts import serializers
from Accounts import models

# using apscheduler to schedule heavy tasks in the background
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.start()



class RegisterAPI(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes = []
    queryset = models.User.objects.all().order_by('-id')
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        data = serializers.UserSerializer(user).data
        return Response({"user": data, "token": token.key}, status=status.HTTP_201_CREATED)


class ChangePasswordAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = serializers.ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response({"detail": "Password has been successfully updated."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
        }, status=status.HTTP_200_OK)


class LogoutView(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.none()

    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except:
            pass
        logout(request)

        return Response({"detail": "User Logged out successfully"})


class PasswordResetRequestView(views.APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            return Response({"detail": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        token = default_token_generator.make_token(user)
        reset_url = f"{settings.PASSWORD_RESET_URL}/{user.pk}/{token}/"

        send_mail(
            "Password Reset Request",
            f"Click the following link to reset your password: {reset_url}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )

        return Response({"detail": "Password reset email sent."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(views.APIView):
    def post(self, request, user_id, token):
        user = get_user_model().objects.get(pk=user_id)
        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        form = SetPasswordForm(user, request.data)
        if form.is_valid():
            form.save()
            return Response({"detail": "Password successfully reset."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid password."}, status=status.HTTP_400_BAD_REQUEST)