# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import factory

from hyputils.memex import models

from .base import ModelFactory


def unique_username(obj):
    """
    Return a unique username for a test user.

    Return a randomly generated username that is guaranteed to be unique within
    a given test run. Uniqueness is necessary because usernames must be unique
    in the DB and generating random usernames in a not-guaranteed-to-be-unique
    way would result in intermittent database errors when running the tests.

    """
    return obj.non_unique_username + "__" + obj.count


def unique_email(obj):
    """
    Return a unique email for a test user.

    Return a randomly generated email that is guaranteed to be unique within
    a given test run. Uniqueness is necessary because emails must be unique
    in the DB and generating random emails in a not-guaranteed-to-be-unique
    way would result in intermittent database errors when running the tests.

    """
    return obj.username + "@" + obj.email_domain


class User(ModelFactory):
    class Meta:
        model = models.User

    class Params:
        # A count that's appended to non-unique usernames to make them unique.
        count = factory.Sequence(lambda n: "%d" % n)
        # The non-unique part of the generated username.
        non_unique_username = factory.Faker("user_name")
        # The domain (following ``@``) part of the generated email address.
        email_domain = factory.Faker("free_email_domain")

    authority = "example.com"
    username = factory.LazyAttribute(unique_username)
    email = factory.LazyAttribute(unique_email)
    registered_date = factory.Faker("date_time_this_decade")
