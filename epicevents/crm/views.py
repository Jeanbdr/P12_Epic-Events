from django.shortcuts import render
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from crm.models import User, Client
from crm.serializers import SignUpSerializer, ClientSerializer, TokenObtentionSerializer


# Create your views here.
class ObtainTokainPairView(TokenObtainPairView):

    """
    This class allow an user connexion by returning him a token authentication
    """

    permission_classes = (AllowAny,)
    serializer_class = TokenObtentionSerializer


class SignupViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ClientSerializer
