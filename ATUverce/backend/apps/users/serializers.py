from rest_framework import serializers
from .models import User, Follow

class UserShortSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'avatar', 'faculty', 'ala_coins', 'is_verified']

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'full_name', 'avatar', 'bio', 'role',
            'group', 'faculty', 'year_of_study', 'skills', 'interests',
            'github', 'linkedin', 'portfolio', 'followers_count',
            'following_count', 'ala_coins', 'is_verified', 'created_at',
            'is_following'
        ]
        read_only_fields = ['ala_coins', 'followers_count', 'following_count', 'is_verified']

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Follow.objects.filter(follower=request.user, following=obj).exists()
        return False


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password', 'password2', 'faculty', 'group', 'year_of_study'
        ]
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
            'faculty': {'required': False},
            'group': {'required': False},
            'year_of_study': {'required': False},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Пароли не совпадают'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user