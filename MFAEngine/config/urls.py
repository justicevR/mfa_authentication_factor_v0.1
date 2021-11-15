"""MFAServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.api.models import User
from django.views.decorators.csrf import csrf_exempt
from apps.api.views import ApiEndpoint, AppList, AppClientList, EnrollUserDetail, EnrolledUserList, EnrollmentDetail, EnrollmentList, UserList, UserDetail, EnrollmentVerify
from apps.api import views

from rest_framework import generics, permissions, serializers
from rest_framework.urlpatterns import format_suffix_patterns

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication

#CHANGES
from apps.dashboard import views as dashboard_views
from apps.users import views as users_views
from apps.self_service import views as service_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('rest_framework.urls')),

    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),


    #access token auth endpoints
    path('token/', views.token),
        
    path('token/revoke/', views.revoke_token),

    #staff users endpoints
    path('api/Users', UserList.as_view()),

    path('api/Users/register', views.register),

    path('api/Users/<int:pk>', UserDetail.as_view()),
    
    #enrollment endpoints
    path('api/factors/totp', EnrollmentList.as_view()),
    path('api/factors/totp/<str:pk>', EnrollmentDetail.as_view()),

    #enrolled users endpoints
    path('api/users', EnrolledUserList.as_view()),
    path('api/users/<str:pk>', EnrollUserDetail.as_view()),
    path('api/users/email/', views.is_enrolled),

    #applications endpoints
    path('api/applications', AppList.as_view()),

    #api clients endpoints
    path('api/apiclients', AppClientList.as_view()),
    path('home', dashboard_views.home, name='home'),

    #user url
    path('registration', users_views.registration_view, name='registration'),
    path('logout', users_views.logout_view, name='logout'),
    path('login', users_views.login_view, name='login'),

    #register app url
    path('register/app', service_views.registerApp_view, name='registerApp'),

    #profile view url
    path('profile', service_views.profile_view, name='profile'),
    path('myapplications', service_views.applications_view, name='myapplications'),
    path('myapplication/details/<int:pk>', service_views.applicationDetails_view, name='details'),

    # Admin urls

    #admin to view details of a given application request
    path('thisapplication/details/<int:pk>', service_views.applicationDetailsAdmin_view, name='detailsAdmin'),


    #registering inviting an app
    path('invite_app/<int:pk>/', service_views.inviteApp_view, name='invite'),

    #rejecting apps admin
    path('reject_app/<int:pk>/', service_views.rejectApp_view, name='reject'),

    #viewing applications for admin
    path('applications',service_views.applicationsAdmin_view, name='view_apps'),

    #api usage
    
    
    #api health
    #enrollment validation L
    path('api/enrollment/verify', EnrollmentVerify.as_view()),
    path('api/enrollment/verify/test', views.enrollVal),
    path('api/enrollment/verify/valid', views.validUser),
    


    #User Manipulation endpoints L
    path('api/users/email/disable', views.enrollDel),
    path('api/users/email/fetch', views.enrollFetch),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)


