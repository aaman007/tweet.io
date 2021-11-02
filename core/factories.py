from django.contrib.auth import get_user_model
import factory
from factory.django import DjangoModelFactory

from accounts.models import Follow
from tweets.models import Tweet

User = get_user_model()

COUNT = User.objects.filter(username__icontains='person').count()


class UserFactory(DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(lambda a: f'{a.first_name}.{a.last_name}@tweet.io'.lower())
    username = factory.Sequence(lambda n: f'person{n + COUNT}')

    class Meta:
        model = User


class FollowFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    follower = factory.SubFactory(UserFactory)

    class Meta:
        model = Follow


class TweetFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    content = factory.Faker("sentence", nb_words=10, variable_nb_words=True)

    class Meta:
        model = Tweet
