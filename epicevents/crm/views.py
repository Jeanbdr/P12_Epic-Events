from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from crm.permissions import (
    CustomersAndContractPermissions,
    EventPermissions,
    EmployeeListPermissions,
    SignupPermissions,
)
from crm.models import User, Client, Contract, Event
from crm.serializers import (
    SignUpSerializer,
    ClientSerializer,
    TokenObtentionSerializer,
    ContractSerializer,
    EventSerializer,
    EmployeeSerializer,
)


# Create your views here.
class ObtainTokainPairView(TokenObtainPairView):

    """
    This class allow an user connexion by returning him a token authentication
    """

    permission_classes = (AllowAny,)
    serializer_class = TokenObtentionSerializer


class SignupViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, SignupPermissions]
    serializer_class = SignUpSerializer


class ClientViewSet(ModelViewSet):
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["last_name", "email"]
    filterset_fields = ["under_contract"]
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated, CustomersAndContractPermissions]
    serializer_class = ClientSerializer


class ContractViewSet(ModelViewSet):
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["client__last_name", "client__email"]
    ordering_fields = ["payment_due"]
    filterset_fields = ["amount", "status"]
    queryset = Contract.objects.all()
    permission_classes = [IsAuthenticated, CustomersAndContractPermissions]
    serializer_class = ContractSerializer


class EventViewSet(ModelViewSet):
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["client__last_name", "client__email"]
    ordering_fields = ["event_date"]
    filterset_fields = ["event_status"]
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated, EventPermissions]
    serializer_class = EventSerializer


class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, EmployeeListPermissions]
    filter_backends = [SearchFilter]
    search_fields = ["role"]
    queryset = User.objects.all()
