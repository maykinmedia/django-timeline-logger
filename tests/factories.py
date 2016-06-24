import factory


class ArticleFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'tests.Article'

    title = factory.Faker('sentence')
    date = factory.Faker('date')


class TimelineLogFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'timeline_logger.TimelineLog'

    content_object = factory.SubFactory(ArticleFactory)
