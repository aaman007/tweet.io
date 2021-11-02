from rest_framework import serializers

from accounts.models import User, Follow


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'followers_count', 'follows_count']


class SingleUserSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'full_name', 'followers_count', 'follows_count', 'is_following']

    def get_is_following(self, obj: User):
        return self.context['request'].user.active_follows().filter(user=obj).exists()


class FollowSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    follower = UserSerializer()

    class Meta:
        model = Follow
        fields = ['user', 'follower']
