import factory


class UserFactory(factory.django.DjangoModelFactory):
    first_name = "Test"
    last_name = "User"
    username = factory.Sequence(lambda n: "user_{0}".format(n))
    email = factory.Sequence(lambda n: "user_{0}@maykinmedia.nl".format(n))
    password = factory.PostGenerationMethodCall("set_password", "testing")

    class Meta:
        model = "auth.User"


class ArticleFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("sentence")
    date = factory.Faker("date")

    class Meta:
        model = "tests.Article"


class TimelineLogFactory(factory.django.DjangoModelFactory):
    content_object = factory.SubFactory(ArticleFactory)

    class Meta:
        model = "timeline_logger.TimelineLog"
