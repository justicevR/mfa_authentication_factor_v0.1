from passlib.totp import TOTP
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.models import get_access_token_model
from rest_framework import generics, permissions, serializers
from django.http.response import Http404, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.api.serializers import AppClientSerializer, AppSerializer, BackupCodeSerializer, EnrolledUserSerializer, EnrollmentSerializer, RegisterSerializer, UserListSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from .models import BackupCode, Enrollment, User, UserEnrolled, App
from ..factors.totp import FactoryTOTP
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny, IsAuthenticated
import requests
import base64, uuid, json, passlib
from ..factors.totp import FactoryTOTP
from oauth2_provider.views.application import ApplicationOwnerIsUserMixin, ApplicationList



# Create your views here.

"""
    Todo:
    ------

    1/ Create and test custom authorization scopes.
    2/ Create and test custom permission scopes.
    3/ Find best encryption algorithm to encrypt secrets in the UserEnrolled Model.
    4/ Design and implement best backup codes generation algorithm for each token enrollment.
    5/ Restrict access to /o/applications.
    6/ ...
"""



# Static TOTP config
totp_defaults = {
    'DIGITS' : 6, 
    'PERIOD' : 30,
    'PERIOD_SKEW' : 0, 
    'ALG' : 'sha1',
    'ISSUER' : 'mfa.server.com',
}

# Instantiate TOTP Factory Class
init = FactoryTOTP(totp_defaults)

def get_basic_auth(client_id, client_secret):

    credential = "{0}:{1}".format(client_id, client_secret)
    basic_auth = base64.b64encode(credential.encode("utf-8")).decode(encoding="utf-8")

    return basic_auth


@api_view(['POST'])
@permission_classes([TokenHasReadWriteScope])
def is_enrolled(request, format=None):
    email = request.POST["account_name"]
    user = UserEnrolled.objects.filter(account_name=email).exists()
    if user:
        return Response(True)
    return Response(False)

@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    '''
    Gets access tokens with client id and client secret.
    '''

    client_id = request.POST['client_id']
    client_secret = request.POST['client_secret']

    res = requests.post(
    'http://0.0.0.0:8000/o/token/', 
        data={
            'grant_type': 'client_credentials',
        },

        headers={
            'Authorization': 'Basic {0}'.format(get_basic_auth(client_id, client_secret)),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )
    return Response(res.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    '''
    Method to revoke access tokens.
    {"token": "<token>"}
    '''

    token = request.POST['token']

    res = requests.post(
        'http://0.0.0.0:8000/o/revoke_token/', 
        data={
            'token': token,
        },

        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )
    # If it goes well return success message (would be empty otherwise) 
    if res.status_code == requests.codes.ok:
        return JsonResponse({'Success': 'Token revoked successfully.'}, res.status_code)
    # Return the error if it goes badly
    return Response(res.json(), res.status_code)


@api_view(['POST'])
@permission_classes([TokenHasReadWriteScope])
def register(request, format=None):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        res = {
            'Success':'Registered staff user successfully.'
        }
        return JsonResponse(res, safe=False, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView, ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserListSerializer(user)
        return JsonResponse(serializer.data, safe=False)


    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserListSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {
                'Success':'Updated staff user successfully.'
            }
            return JsonResponse(res, safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        res = {
            'Success':'Deleted staff user successfully.'
        }
        return JsonResponse(res, safe=False, status=status.HTTP_204_NO_CONTENT)


class UserList(APIView, ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)


class EnrollUserDetail(APIView, ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]

    def get_object(self, pk):
        try:
            return UserEnrolled.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = EnrolledUserSerializer(user)
        return JsonResponse(serializer.data, safe=False)

    def delete(self, request, pk, format=None):
        user_enrolled = self.get_object(pk)
        user_enrolled.delete()
        res = {
            'Success':'Deleted enrolled user successfully.'
        }
        return JsonResponse(res, safe=False, status=status.HTTP_204_NO_CONTENT)



class EnrolledUserList(APIView, ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]

    def get(self, request, format=None):
        enrolledusers = UserEnrolled.objects.all()
        serializer = EnrolledUserSerializer(enrolledusers, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        new_post_req = self.request.POST.copy()
        new_post_req.__setitem__('user_id', '{}'.format(uuid.uuid4())) # Generated User ID should be purely cryptographically random
        serializer = EnrolledUserSerializer(data=new_post_req)

        if serializer.is_valid():
            serializer.save()
            # After successfully enrolling the user; enroll their tokens.
            # Generate enrollment id, totp factory, wallet secret

            ENROLLMENT_ID = '{}'.format(uuid.uuid4())
            USER_ID = new_post_req.get('user_id')

            # Prepare TOTP Factory.
            # Create TOTP Factory instance AND Base64'd QRCode to be stored in the database.

            SECRET = json.dumps(dict({str("{}".format(uuid.uuid4())): str(passlib.totp.generate_secret(entropy=256))})) # This is a wallet secret dict for storing TOTP Factory secret keys.

            INIT_FACTORY = init.create_factory(SECRET) 
            INSTANCE = init.get_totp_instance(INIT_FACTORY)
            STORED_INSTANCE = init.store_totp_instance(INSTANCE)
            KEY = init.get_key(INIT_FACTORY, STORED_INSTANCE)
            b64_qrcode = init.get_qrcode(init.config_client(INIT_FACTORY, new_post_req.get('account_name'), KEY))
            
            

            UserEnrolled.objects.filter(pk=USER_ID).update(
                factory = STORED_INSTANCE,
                secret = SECRET
            )
            
            Enrollment.objects.create(
                enrollment_id = ENROLLMENT_ID,
                b64_QRCode = b64_qrcode,
                user_id_id = USER_ID
            )
            
            serialize = Enrollment.objects.get(pk=ENROLLMENT_ID)
            serializer = EnrollmentSerializer(serialize)


            return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)


class AppList(APIView, ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]

    def get(self, request, format=None):
        apps = App.objects.all()
        serializer = AppSerializer(apps, many=True)
        return JsonResponse(serializer.data, safe=False)


class BackupCodeList(APIView, ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]

    def get(self, request, format=None):
        backup_codes = BackupCode.objects.all()
        serializer = BackupCodeSerializer(backup_codes, many=True)
        return JsonResponse(serializer.data, safe=False)


class EnrollmentList(APIView, ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]

    def get_object(self, pk):
        try:
            return Enrollment.objects.get(pk=pk)
        except Enrollment.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        enrollments = Enrollment.objects.all()
        serializer = EnrollmentSerializer(enrollments, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        # Verify / validate totp token

        totp = request.POST['totp']
        factor = request.POST['factor'] # Enrollment ID

        enrollment = self.get_object(factor)
        user_enrolled = UserEnrolled.objects.get(pk=enrollment.user_id_id)
        instance = user_enrolled.factory
        secret = user_enrolled.secret

        factory = init.create_factory(secret=secret)
        response = init.verify_token(totp, factory, instance)

        return Response(str(response))


class EnrollmentDetail(APIView, ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]

    def get_object(self, pk):
        try:
            return Enrollment.objects.get(pk=pk)
        except Enrollment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        # Get TOTP for specific TOTP enrollment

        user = self.get_object(pk)
        serializer = EnrollmentSerializer(user)
        return JsonResponse(serializer.data, safe=False)

    def delete(self, request, pk, format=None):
        # Delete TOTP token enrollment

        enrollment = self.get_object(pk)
        enrollment.delete()
        res = {
            'Success':'Deleted token enrollment successfully.'
        }
        return JsonResponse(res, safe=False, status=status.HTTP_204_NO_CONTENT)


class AppClientList(APIView, ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]

    def get(self, request, format=None):
        api_clients = App.objects.all()
        serializer = AppClientSerializer(api_clients, many=True)
        return JsonResponse(serializer.data, safe=False)


class ApiEndpoint(ProtectedResourceView):
    def get(self, request, pk, format=None):
        return JsonResponse('Hello, Welcome to our MFA Engine!')


#CHANGES STARTS HERE
#class for validating user enrollment token 27/09/2021 -- DONE
class EnrollmentVerify(APIView, ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]

    def get_object(self, pk):
        try:
            return Enrollment.objects.get(pk=pk)
        except Enrollment.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        # Verify / validate totp token

        totp = request.POST['totp']
        factor = request.POST['factor'] # Enrollment ID

        enrollment = self.get_object(factor)
        user_enrolled = UserEnrolled.objects.get(pk=enrollment.user_id_id)
        instance = user_enrolled.factory
        secret = user_enrolled.secret

        factory = init.create_factory(secret=secret)
        response = init.verify_token(totp, factory, instance)

        list = str(response)
        sub = "TotpMatch"
        if sub in list:
            Enrollment.objects.filter(enrollment_id=factor).update(validated=True)
            print(response)
            return Response(str(response))
        print(response)
        return Response(str(response))


#CHANGES
#this function to delete user 20/sept/2021 -- DONE
@api_view(['POST'])
@permission_classes([TokenHasReadWriteScope])
def enrollDel(request, format=None):
    email = request.POST["account_name"]
    user = UserEnrolled.objects.filter(account_name=email)
    if user:
        user.delete()
        res = {
            'Success':'Deleted enrolled user successfully.'
        }
        return JsonResponse(res, safe=False, status=status.HTTP_204_NO_CONTENT)
    return Response(False)

#CHANGES
#this function to check validated user AND delete when not verify_token --DONE
@api_view(['POST'])
@permission_classes([TokenHasReadWriteScope])
def enrollVal(request, format=None):
    id = request.POST["enrollment_id"]
    email = request.POST["account_name"]
    user = UserEnrolled.objects.filter(account_name=email)
    uservalid = Enrollment.objects.filter(enrollment_id=id).values('validated')
    valid = uservalid[0]['validated']
    print(valid)
    if valid == False:
        user.delete()
        return Response(False)
    return Response(True)

#CHANGES
#function to check if user is VALID 28/7/2021 ----- ON PROGRESS
@api_view(['POST'])
@permission_classes([TokenHasReadWriteScope])
def validUser(request, format=None):
    email = request.POST["account_name"]
    user = UserEnrolled.objects.filter(account_name=email).exists()
    if user == True:
        uservalid = Enrollment.objects.filter(user_id_id=email).values('validated')
        print(uservalid)
        # valid = uservalid[0]['validated']
        # print(valid)
        if uservalid == False:
            return Response(True)
        return Response('HEEE')
    return Response(False)

#CHANGES
#this function to fetch enrollment_id user 21/sept/2021 --- NOT USED YET
@api_view(['GET'])
@permission_classes([TokenHasReadWriteScope])
def enrollFetch(request, format=None):
    email = request.POST["account_name"]
    users = Enrollment.objects.filter(user_id_id=email)
    serializer = EnrollmentSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)



