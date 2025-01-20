# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime
import re

import sqlalchemy as sa
from sqlalchemy.ext.hybrid import Comparator, hybrid_property
from sqlalchemy.ext.declarative import declared_attr

from hyputils.memex._compat import string_types
from hyputils.memex.db import Base
from hyputils.memex.util.user import split_user
from hyputils.memex.security import security

USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 30
USERNAME_PATTERN = "(?i)^[A-Z0-9._]+$"
EMAIL_MAX_LENGTH = 100
DISPLAY_NAME_MAX_LENGTH = 30


def _normalise_username(username):
    # We normalize usernames by dots and case in order to discourage attempts
    # at impersonation.
    return sa.func.lower(sa.func.replace(username, sa.text("'.'"), sa.text("''")))


class UsernameComparator(Comparator):
    """
    Custom comparator for :py:attr:`~h.models.user.User.username`.

    This ensures that all lookups against the username property, such as

        session.query(User).filter_by(username='juanwood')

    use the normalised username for the lookup and appropriately normalise the
    RHS of the query. This means that a query like the one above will
    correctly find a user with a username of "Juan.Wood", for example.
    """

    def operate(self, op, other, **kwargs):
        return op(
            _normalise_username(self.__clause_element__()),
            _normalise_username(other),
            **kwargs
        )


class UserIDComparator(Comparator):
    """
    Custom comparator for :py:attr:`~h.models.user.User.userid`.

    A user's userid is a compound property which depends on their username
    and their authority. A naive comparator for this property would generate
    SQL like the following:

        ... WHERE 'acct:' || username || '@' || authority = ...

    This would be slow, due to the lack of an index on the LHS expression.
    While we could add a functional index on this expression, we can also take
    advantage of the existing index on (normalised_username, authority), which
    is what this comparator does.

    A query such as

        session.query(User).filter_by(userid='acct:luis.silva@example.com')

    will instead generate

        WHERE
            (lower(replace(username,     '.', '')), authority    ) =
            (lower(replace('luis.silva', '.', '')), 'example.com')
    """

    def __init__(self, username, authority):
        self.username = username
        self.authority = authority

    def __clause_element__(self):
        return sa.tuple_(_normalise_username(self.username), self.authority)

    def __eq__(self, other):
        """
        Compare the userid for equality with `other`.

        `other` can be anything plausibly on the RHS of a comparison, which
        can include other SQL clause elements or expressions, as in

            User.userid == sa.tuple_(User.username, Group.authority)

        or literals, as in

            User.userid == 'acct:miruna@example.com'

        We treat the literal case specially, and split the string into
        username and authority ourselves. If the string is not a well-formed
        userid, the comparison will always return False.
        """
        if isinstance(other, string_types):
            try:
                val = split_user(other)
            except ValueError:
                # The value being compared isn't a valid userid
                return False
            else:
                other = sa.tuple_(_normalise_username(val["username"]), val["domain"])
        return self.__clause_element__() == other

    def in_(self, userids):
        others = []
        for userid in userids:
            try:
                val = split_user(userid)
            except ValueError:
                continue

            other = sa.tuple_(_normalise_username(val["username"]), val["domain"])
            others.append(other)

        if not others:
            return False

        return self.__clause_element__().in_(others)


class User(Base):
    __tablename__ = "user"

    @declared_attr
    def __table_args__(cls):  # noqa: N805
        return (
            # (email, authority) must be unique
            sa.UniqueConstraint("email", "authority"),
            # (normalised username, authority) must be unique. This index is
            # also critical for making user lookups fast.
            sa.Index(
                "ix__user__userid",
                _normalise_username(cls.username),
                cls.authority,
                unique=True,
            ),
        )

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    #: Username as chosen by the user on registration
    _username = sa.Column("username", sa.UnicodeText(), nullable=False)

    #: The "authority" for this user. This represents the "namespace" in which
    #: this user lives. By default, all users are created in the namespace
    #: corresponding to `request.domain`, but this can be overridden with the
    #: `h.authority` setting.
    authority = sa.Column("authority", sa.UnicodeText(), nullable=False)

    #: The display name which will be used when rendering an annotation.
    display_name = sa.Column(sa.UnicodeText())

    #: A short user description/bio
    description = sa.Column(sa.UnicodeText())

    #: A free-form column to allow the user to say where they are
    location = sa.Column(sa.UnicodeText())

    #: The user's URI/link on the web
    uri = sa.Column(sa.UnicodeText())

    #: The user's ORCID ID
    orcid = sa.Column(sa.UnicodeText())

    identities = sa.orm.relationship(
        "UserIdentity", backref="user", cascade="all, delete-orphan"
    )

    @hybrid_property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @username.comparator
    def username(cls):  # noqa: N805
        return UsernameComparator(cls._username)

    @hybrid_property
    def userid(self):
        return "acct:{username}@{authority}".format(
            username=self.username, authority=self.authority
        )

    @userid.comparator
    def userid(cls):  # noqa: N805
        return UserIDComparator(cls.username, cls.authority)

    email = sa.Column(sa.UnicodeText())

    last_login_date = sa.Column(
        sa.TIMESTAMP(timezone=False),
        default=datetime.datetime.utcnow,
        server_default=sa.func.now(),
        nullable=False,
    )
    registered_date = sa.Column(
        sa.TIMESTAMP(timezone=False),
        default=datetime.datetime.utcnow,
        server_default=sa.func.now(),
        nullable=False,
    )

    @sa.orm.validates("email")
    def validate_email(self, key, email):
        if email is None:
            return email

        if len(email) > EMAIL_MAX_LENGTH:
            raise ValueError(
                "email must be less than {max} characters "
                "long".format(max=EMAIL_MAX_LENGTH)
            )
        return email

    @sa.orm.validates("_username")
    def validate_username(self, key, username):
        if not USERNAME_MIN_LENGTH <= len(username) <= USERNAME_MAX_LENGTH:
            raise ValueError(
                "username must be between {min} and {max} "
                "characters long".format(
                    min=USERNAME_MIN_LENGTH, max=USERNAME_MAX_LENGTH
                )
            )

        if not re.match(USERNAME_PATTERN, username):
            raise ValueError(
                "username must have only letters, numbers, " "periods, and underscores."
            )

        return username

    @classmethod
    def get_by_email(cls, session, email, authority):
        """Fetch a user by email address."""
        if email is None:
            return None

        return (
            session.query(cls)
            .filter(
                sa.func.lower(cls.email) == email.lower(), cls.authority == authority
            )
            .first()
        )

    @classmethod
    def get_by_username(cls, session, username, authority):
        """Fetch a user by username."""
        return (
            session.query(cls)
            .filter(cls.username == username, cls.authority == authority)
            .first()
        )

    def __acl__(self):
        terms = []

        # auth_clients that have the same authority as the user
        # may update the user
        user_update_principal = "client_authority:{}".format(self.authority)
        terms.append((security.Allow, user_update_principal, "update"))

        terms.append(security.DENY_ALL)

        return terms

    def __repr__(self):
        return "<User: %s>" % self.username
