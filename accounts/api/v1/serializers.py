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
    followers_count = serializers.SerializerMethodField()
    follows_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'full_name', 'followers_count', 'follows_count']

    def get_followers_count(self, obj: User):
        if hasattr(obj, 'followers_count'):
            return getattr(obj, 'followers_count')
        return obj.active_followers().count()

    def get_follows_count(self, obj: User):
        if hasattr(obj, 'follows_count'):
            return getattr(obj, 'follows_count')
        return obj.active_follows().count()


class SingleUserSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    follows_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'full_name', 'followers_count', 'follows_count', 'is_following']

    def get_is_following(self, obj: User):
        return self.context['request'].user.active_follows().filter(user=obj).exists()

    def get_followers_count(self, obj: User):
        return obj.active_followers().count()

    def get_follows_count(self, obj: User):
        return obj.active_follows().count()


class FollowSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    follower = UserSerializer()

    class Meta:
        model = Follow
        fields = ['user', 'follower']
