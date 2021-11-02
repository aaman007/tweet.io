import random

from django.core.management.base import BaseCommand
from django.db import transaction

from core.factories import UserFactory, FollowFactory, TweetFactory

NUM_USERS = 1000
MAX_FOLLOWS_PER_USER = 20  # < NUM_USERS
NUM_TWEETS = 10000


class Command(BaseCommand):
    help = 'Creates dummy data for testing'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Creating new users...")
        users = [UserFactory() for _ in range(NUM_USERS)]

        self.stdout.write("Creating new follow relations...")
        for follower in range(NUM_USERS):
            follows = random.randint(0, MAX_FOLLOWS_PER_USER)
            available_users = [i for i in range(NUM_USERS) if i != follower]

            for _ in range(follows):
                user = random.choice(available_users)
                FollowFactory(user=users[user], follower=users[follower])
                available_users.remove(user)

        self.stdout.write("Creating new tweets...")
        for _ in range(NUM_TWEETS):
            user = random.choice(users)
            TweetFactory(user=user)

        self.stdout.write("Created test data successfully...")
