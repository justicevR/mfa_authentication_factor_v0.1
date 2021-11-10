from .models import User, App, UserEnrolled, Enrollment, BackupCode
from rest_framework import generics, permissions, serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


# first we define the serializers
class UserListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class EnrolledUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = UserEnrolled.objects.create(**validated_data)
        return user

    class Meta:
        model = UserEnrolled
        fields = ('user_id', 'account_name', 'app_id')
        extra_kwargs = {
            'user_id': {'write_only': True}
        }


class RegisterSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2')
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user


class EnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment
        fields = '__all__'


class AppSerializer(serializers.ModelSerializer):

    class Meta:
        model = App
        fields = ['id', 'name', 'domain', 'org_name', 'user']


class BackupCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BackupCode
        fields = '__all__'


class AppClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = App
        fields = ['id', 'client_id', 'client_type', 'authorization_grant_type', 'redirect_uris', 'skip_authorization', 'algorithm', 'created', 'updated']