from django.shortcuts import render
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from crm.permissions import CustomersAndContractPermissions, EventPermissions
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
    filter_backends = [SearchFilter]
    search_fields = ["last_name", "email"]
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated, CustomersAndContractPermissions]
    serializer_class = ClientSerializer


class ContractViewSet(ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ["client__last_name", "client__email"]
    queryset = Contract.objects.all()
    permission_classes = [IsAuthenticated, CustomersAndContractPermissions]
    serializer_class = ContractSerializer


class EventViewSet(ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ["client__last_name", "client__email"]
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated, EventPermissions]
    serializer_class = EventSerializer
