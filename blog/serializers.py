from . import models


from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.sessions.models import Session

UserModel = get_user_model()


class JobPostSerializer(serializers.Serializer):
    user = serializers.ReadOnlyField(source="user.name")

    class Meta:
        model = models.JobPost
        fields = "__all__"


class UserSerializer(serializers.Serializer):
    class Meta:
        model = models.SiteUser
        fields = ["name"]
        lookup_field = "slug"


class UserRegistrationSerializer(serializers.ModelSerializer):
    session_key = serializers.SerializerMethodField(read_only=True)
    author_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserModel
        fields = ["session_key", "author_details"]

    def create(self, clean_data):
        email = clean_data.pop("email")
        password = clean_data.pop("password")

        user_obj = UserModel.objects.create_user(
            email=email, password=password, **clean_data
        )
        user_obj.username = email  # remember to create username field
        user_obj.save()
        return user_obj

    def get_session_key(self, obj):
        session = Session.objects.filter(
            session_key=self.context["request"].session.session_key
        ).first()
        return session.session_key if session else None


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    session_key = serializers.SerializerMethodField(read_only=True)
    user_details = serializers.SerializerMethodField(read_only=True)

    def get_session_key(self, obj):
        session = Session.objects.filter(
            session_key=self.context["request"].session.session_key
        ).first()
        return session.session_key if session else None

    def get_user_details(self, obj):
        return UserSerializer(obj).data

    def check_user(self, clean_data):
        user = authenticate(
            username=clean_data["email"], password=clean_data["password"]
        )

        if not user:
            raise serializers.ValidationError("User not Found!")
        return user
