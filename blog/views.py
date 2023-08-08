from django.shortcuts import render
from .models import JobPost, SiteUser  # , Applications
from rest_framework import generics, status, permissions, filters
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from . import serializers

from .pagination import StandardResultSetPagination
import django_filters
from .permissions import IsUserOrReadOnly
from .validations import registration_validation, validate_email, validate_password
from django.contrib.auth import get_user_model, login, logout

from django.conf import settings


# Create your views here.


def tempView(request):
    return render(request, "temp.html")


class SiteUserList(generics.ListAPIView):
    queryset = SiteUser.objects.all()
    serializer_class = serializers.UserSerializer


class SiteUserDetails(generics.RetrieveAPIView):
    queryset = SiteUser.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = "slug"


class JobPostList(generics.ListAPIView):
    queryset = JobPost.objects.all()
    serializer_class = serializers.JobPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultSetPagination
    filterset_fields = ["poster", "status", "created_on"]
    search_fields = [
        "title",
    ]
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

    ordering_fields = [
        "created_on",
        "title",
    ]
    ordering = ["-created_on", "title"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.user)


class JobPostDetails(generics.RetrieveAPIView):
    queryset = JobPost.objects.all()
    serializer_class = serializers.JobPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly]

    lookup_field = "slug"


class SiteUserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def job_post(self, request):
        clean_data = registration_validation(request.data)
        serializer = serializers.UserRegistrationSerializer(data=clean_data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                serializer = serializers.UserRegistrationSerializer(
                    user, context={"request": request}
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SiteUserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def job_post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)

        serializer = serializers.UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            serializer = serializers.UserLoginSerializer(
                user, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)


class SiteUserLogout(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


"""class ApplicationList(generics.ListAPIView):
    queryset = Applications.objects.all()
    serializer_class = serializers.ApplicationSerializer


class ApplicationDetails(generics.RetrieveAPIView):
    queryset = Applications.objects.all()
    serializer_class = serializers.ApplicationSerializer"""
