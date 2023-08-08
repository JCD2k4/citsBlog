from django.urls import path, include
from . import views

"""urlpatterns = [
    path("", views.tempView),
    path("api/postings", views.UserList.as_view()),
    path("api/postings/<int: pk>", views.UserDetail.as_view()),
    path(),
]"""

urlpatterns = [
    path("", views.tempView),
    path("api-auth/", include("rest_framework.urls")),
    path("api/jobs", views.JobPostList.as_view(), name="api_post_list"),
    path(
        "api/jobs/<slug:slug>", views.JobPostDetails.as_view(), name="api_post_details"
    ),
    path("api/users", views.SiteUserList.as_view(), name="api_user_list"),
    path(
        "api/users/<slug:slug>",
        views.SiteUserDetails.as_view(),
        name="api_user_details",
    ),
    path(
        "api/user/register", views.SiteUserRegister.as_view(), name="api_user_register"
    ),
    path("api/user/login", views.SiteUserLogin.as_view(), name="api_user_login"),
    path("api/user/logout", views.SiteUserLogout.as_view(), name="api_user_logout"),
]
