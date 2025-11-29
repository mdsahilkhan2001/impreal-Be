from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import requests
from django.conf import settings

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""

    role = serializers.SerializerMethodField()
    role_label = serializers.CharField(source='get_role_display', read_only=True)
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'role', 'role_label', 'phone', 'company', 'avatar', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_role(self, obj):
        return obj.role

    def get_avatar(self, obj):
        if not obj.avatar:
            return None
        request = self.context.get('request') if hasattr(self, 'context') else None
        url = obj.avatar.url
        if request:
            return request.build_absolute_uri(url)
        return url


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""

    avatar = serializers.ImageField(required=False, allow_null=True)
    remove_avatar = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'company', 'avatar', 'remove_avatar']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone': {'required': False},
            'company': {'required': False},
        }

    def update(self, instance, validated_data):
        remove_avatar = validated_data.pop('remove_avatar', False)
        avatar = validated_data.pop('avatar', None)

        if remove_avatar and instance.avatar:
            instance.avatar.delete(save=False)
            instance.avatar = None

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if avatar is not None:
            instance.avatar = avatar

        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for updating the user's password"""

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect')
        return value

    def validate(self, attrs):
        if attrs.get('old_password') == attrs.get('new_password'):
            raise serializers.ValidationError('New password must be different from the current password')
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(min_length=6, max_length=6)


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
        return attrs


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users (registration)"""
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'role', 'phone', 'company']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'BUYER'),
            phone=validated_data.get('phone', ''),
            company=validated_data.get('company', '')
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer that returns user data with tokens"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['identifier'] = serializers.CharField(write_only=True, required=False)
        self.fields[self.username_field].required = False
        self.fields[self.username_field].allow_blank = True

    def validate(self, attrs):
        # Expect a captcha token from client under 'captcha' or 'g-recaptcha-response'
        captcha_token = attrs.pop('captcha', None) or attrs.pop('g-recaptcha-response', None)
        recaptcha_secret = getattr(settings, 'RECAPTCHA_SECRET', '')

        if not recaptcha_secret:
            # If no server-side secret configured, allow login (use only during local/dev)
            pass
        else:
            if not captcha_token:
                raise serializers.ValidationError({'captcha': 'Captcha token is required.'})

            try:
                resp = requests.post(
                    'https://www.google.com/recaptcha/api/siteverify',
                    data={'secret': recaptcha_secret, 'response': captcha_token},
                    timeout=5,
                )
                result = resp.json()
            except Exception:
                raise serializers.ValidationError({'captcha': 'Unable to validate captcha. Try again later.'})

            # If siteverify returns success false -> reject
            if not result.get('success'):
                raise serializers.ValidationError({'captcha': 'Captcha verification failed.'})

            # If reCAPTCHA v3, optionally check score (fail if too low)
            score = result.get('score')
            if score is not None:
                try:
                    threshold = float(getattr(settings, 'RECAPTCHA_MIN_SCORE', 0.3))
                except Exception:
                    threshold = 0.3
                if score < threshold:
                    raise serializers.ValidationError({'captcha': 'Captcha score too low.'})

        identifier = attrs.pop('identifier', None)
        if identifier and not attrs.get(self.username_field):
            identifier = identifier.strip()
            user_obj = User.objects.filter(
                Q(email__iexact=identifier) | Q(username__iexact=identifier)
            ).first()

            if not user_obj:
                raise AuthenticationFailed('No active account found with the given credentials')

            attrs[self.username_field] = getattr(user_obj, self.username_field)

        if not attrs.get(self.username_field):
            raise serializers.ValidationError({'identifier': 'Email or username is required'})

        data = super().validate(attrs)

        # Add user data to the response
        data['user'] = UserSerializer(self.user, context=self.context).data
        
        return data
