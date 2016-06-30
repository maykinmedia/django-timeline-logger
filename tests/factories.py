import factory


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'auth.User'

    first_name = 'Test'
    last_name = 'User'
    username = factory.Sequence(lambda n: 'user_{0}'.format(n))
    email = factory.Sequence(lambda n: 'user_{0}@maykinmedia.nl'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'testing')


class ArticleFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'tests.Article'

    title = factory.Faker('sentence')
    date = factory.Faker('date')


class TimelineLogFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'timeline_logger.TimelineLog'

    content_object = factory.SubFactory(ArticleFactory)
