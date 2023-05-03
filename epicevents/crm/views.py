from django.shortcuts import render
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from crm.models import User, Client, Contract, Event
from crm.serializers import (
    SignUpSerializer,
    ClientSerializer,
    TokenObtentionSerializer,
    ContractSerializer,
    EventSerializer,
)


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


class ContractViewSet(ModelViewSet):
    # queryset = Contract.objects.all()
    def get_queryset(self):
        queryset = Contract.objects.filter(client=self.kwargs["clients_pk"])
        return queryset

    permission_classes = (IsAuthenticated,)
    serializer_class = ContractSerializer


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer
