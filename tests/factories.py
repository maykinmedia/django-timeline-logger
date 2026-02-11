from django.contrib.auth.models import User

import factory


class UserFactory(factory.django.DjangoModelFactory[User]):
    first_name = "Test"
    last_name = "User"
    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.Sequence(lambda n: f"user_{n}@maykinmedia.nl")

    class Meta:
        model = "auth.User"
        skip_postgeneration_save = True

    @factory.post_generation
    def password(obj: User, create, extracted, **kwargs):
        obj.set_password(extracted or "testing")
        if create:
            obj.save()


class ArticleFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("sentence")
    date = factory.Faker("date")

    class Meta:
        model = "tests.Article"


class TimelineLogFactory(factory.django.DjangoModelFactory):
    content_object = factory.SubFactory(ArticleFactory)

    class Meta:
        model = "timeline_logger.TimelineLog"
