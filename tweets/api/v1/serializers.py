from rest_framework import serializers

from accounts.api.v1.serializers import BasicUserSerializer
from tweets.models import Tag, Tweet


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title']

    def to_representation(self, instance):
        """
        Intercepts the serialized data and converts the tag dictionary to string
        :param instance:
        :return: string
        """

        data = super().to_representation(instance)
        return data['title']


class TweetSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'user', 'content', 'tags', 'created_at']

    def to_representation(self, instance):
        """
        Intercepts the serialized data and serializes tag instances
        :param instance:
        :return: OrderedDict
        """

        data = super().to_representation(instance)
        data['tags'] = TagSerializer(instance.tags, many=True).data
        return data

    def to_internal_value(self, data):
        """
        Intercepts data passed by POST/PUT/PATCH requests, where tags are raw strings
        Converts those to ids
        :param data:
        :return: OrderedDict
        """

        if 'tags' in data:
            data['tags'] = Tag.objects.get_or_create_ids(data['tags'])
        return super().to_internal_value(data)
