from django.db import models


class TagManager(models.Manager):
    def get_or_create_ids(self, tags):
        """
        Receives a string or list of strings. When a string is received converts it to list
        Fetches or create new Tag entries for the received strings
        :param tags:
        :return: list of ids
        """

        if isinstance(tags, str):
            tags = [tags]
        return [self.get_or_create(title=tag)[0].id for tag in tags if len(tag) <= 60]


class TweetManager(models.Manager):
    def followed_users_tweets(self, user):
        """
        Given a user, finds all the tweets made by the users that the given user follows
        :param user:
        :return: QuerySet of Tweet Instances
        """

        followed_users = [followed.user_id for followed in user.follows.only('user_id')]
        return self.filter(user__in=followed_users)

    def follower_tweets(self, user):
        """
        Given a user, finds all the tweets made by the users that follows the given user
        :param user:
        :return: QuerySet of Tweet Instances
        """

        follower_ids = [follower.user_id for follower in user.followers.only('user_id')]
        return self.filter(user__in=follower_ids)
