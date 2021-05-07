import datetime
import random

import factory
import pytz
from django.utils.text import slugify
from factory import django, fuzzy
from faker import Faker

from apps.recipes.models import Recipe
from users_api.factory import YamdbUserFactory


class CategoryFactory(django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f'Category-{n}')

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.name)


class GenreFactory(django.DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.Sequence(lambda n: f'Genre-{n}')

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.name)


class TitleFactory(django.DjangoModelFactory):
    category = factory.SubFactory(CategoryFactory)

    @factory.lazy_attribute
    def name(self):
        fake = Faker(locale='en-US')
        return fake.catch_phrase()

    @factory.lazy_attribute
    def year(self):
        fake = Faker()
        return fake.year()

    @factory.lazy_attribute
    def description(self):
        fake = Faker()
        sentences = random.randint(2, 7)
        return ' '.join(fake.paragraphs(nb=sentences))

    @factory.post_generation
    def genre(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for one_genre in extracted:
                if random.random() < 0.3:
                    self.genre.add(one_genre)

    class Meta:
        model = Title


class ReviewFactory(django.DjangoModelFactory):
    author = factory.SubFactory(YamdbUserFactory)

    score = fuzzy.FuzzyInteger(1, 10)

    title = factory.SubFactory(TitleFactory)

    @factory.lazy_attribute
    def text(self):
        fake = Faker()
        sentences = random.randint(2, 12)
        return ' '.join(fake.paragraphs(nb=sentences))

    @factory.lazy_attribute
    def pub_date(self):
        fake = Faker()
        from_date = datetime.datetime.strptime(str(self.title.year), '%Y')
        return fake.date_time_ad(
            start_datetime=from_date,
            end_datetime='now',
            tzinfo=pytz.UTC,
        )

    class Meta:
        model = Review


class CommentsFactory(django.DjangoModelFactory):
    author = factory.SubFactory(YamdbUserFactory)
    review = factory.SubFactory(ReviewFactory)

    @factory.lazy_attribute
    def text(self):
        fake = Faker()
        sentences = random.randint(1, 5)
        return ' '.join(fake.paragraphs(nb=sentences))

    @factory.lazy_attribute
    def pub_date(self):
        fake = Faker()
        from_datetime = self.review.pub_date
        return fake.date_time_ad(
            start_datetime=from_datetime,
            end_datetime='now',
            tzinfo=pytz.UTC,
        )

    class Meta:
        model = Comment