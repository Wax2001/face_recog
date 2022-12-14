from apps.processing.models import User, Record
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'user_working_hours', 'user_salary', 'user_images')

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id')

class NotApprovedUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'user_images')

class UserApproveSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    is_approved = serializers.BooleanField(default=True)

    class Meta:
        fields = ('id', 'is_approved',)


class UserSigninSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('id', 'user', 'user_occurences', 'check_in_time', 'check_out_time')