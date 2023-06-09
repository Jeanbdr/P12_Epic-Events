from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password

from crm.models import User, Client, Contract, Event


class TokenObtentionSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super(TokenObtentionSerializer, cls).get_token(user)
        token["username"] = user.username
        return token


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "role",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
            "password": {"write_only": True},
        }

    def validate_password(self, value: str) -> str:
        if value is not None:
            return make_password(value)

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            username=validated_data["username"],
            role=validated_data["role"],
            password=validated_data["password"],
        )
        if user.role == "MANAGEMENT":
            user.is_staff = True
            user.is_superuser = True
            user.save()
        else:
            user.is_staff = True
            user.save()
        return user


class ClientSerializer(serializers.ModelSerializer):
    phone = serializers.IntegerField(
        validators=[UniqueValidator(queryset=Client.objects.all())]
    )
    mobile = serializers.IntegerField(
        validators=[UniqueValidator(queryset=Client.objects.all())]
    )

    class Meta:
        model = Client
        fields = "__all__"
        read_only_fields = ["id", "date_created", "date_updated", "sales_contact"]

    @property
    def user(self):
        request = self.context.get("request", None)
        if request:
            return request.user

    def create(self, validated_data):
        client = Client.objects.create(
            under_contract=validated_data["under_contract"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            phone=validated_data["phone"],
            mobile=validated_data["mobile"],
            company_name=validated_data["company_name"],
            sales_contact=self.user,
        )
        return client


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"
        read_only_fields = [
            "id",
            "sales_contact",
            "date_created",
            "date_updated",
        ]

    @property
    def user(self):
        request = self.context.get("request", None)
        if request:
            return request.user

    def validate_client(self, client):
        if not client.under_contract:
            raise ValidationError("Client must be signed before create contract")
        return client

    def create(self, validated_data):
        client = Client.objects.get(id=self.context["view"].kwargs["clients_pk"])
        contract = Contract.objects.create(
            sales_contact=self.user,
            client=client,
            status=validated_data["status"],
            amount=validated_data["amount"],
            payment_due=validated_data["payment_due"],
        )
        return contract


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = [
            "id",
            "client",
            "date_created",
            "date_updated",
        ]

    def validate_support_contact(self, support_contact):
        if support_contact.role != "SUPPORT":
            raise ValidationError("This user is not a support user")
        return support_contact

    def validate_contract(self, contract):
        if not contract.status:
            raise ValidationError("You can't create an event if contract is not signed")
        return contract

    def create(self, validated_data):
        event = Event.objects.create(
            client_id=self.context["view"].kwargs["clients_pk"],
            contract_id=self.context["view"].kwargs["contract_pk"],
            event_status=validated_data["event_status"],
            support_contact=validated_data["support_contact"],
            attendees=validated_data["attendees"],
            event_date=validated_data["event_date"],
            note=validated_data["note"],
        )
        return event


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "role", "username", "first_name", "last_name", "email"]
