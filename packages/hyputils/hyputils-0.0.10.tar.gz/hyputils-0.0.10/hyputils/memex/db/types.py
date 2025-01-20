# -*- coding: utf-8 -*-

"""Custom SQLAlchemy types for use with the Annotations API database."""
from __future__ import unicode_literals

from hyputils.memex._compat import string_types
import binascii
import base64
import uuid

from sqlalchemy import types
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import DontWrapMixin


# A magic byte (expressed as two hexadecimal nibbles) which we use to expand a
# 15-byte ElasticSearch flake ID into a 16-byte UUID.
#
# The UUID specification defines UUIDs as taking the form
#
#     xxxxxxxx-xxxx-Mxxx-Nxxx-xxxxxxxxxxxx
#
# in the canonical hexadecimal representation. M and N represent the UUID
# version and variant fields respectively. The four bits M can take values {1,
# 2, 3, 4, 5} in specified UUID types, and the first three bits of N can take
# the values {8, 9, 0xa, 0xb} in specified UUID types.
#
# In order to expand a 15-byte ElasticSearch flake ID into a value that can be
# stored in the UUID field, we insert the magic nibbles 0xe, 0x5 into the
# version and variant fields respectively. These values are disjoint with any
# specified UUID so the resulting UUID can be distinguished from those
# generated by, for example, PostgreSQL's uuid_generate_v1mc(), and mapped back
# to a 20-char ElasticSearch flake ID.
ES_FLAKE_MAGIC_BYTE = ["e", "5"]


class InvalidUUID(Exception, DontWrapMixin):
    pass


class URLSafeUUID(types.TypeDecorator):

    """
    Expose UUIDs as URL-safe base64-encoded strings.

    Fields decorated with this type decorator use PostgreSQL UUID fields for
    storage, but expose URL-safe strings in the application.

    This type decorator will handle the transformation between any UUID and a
    URL-safe, base64-encoded string version of that UUID (which will be 22
    characters long). In addition, it will transparently map post-v1.4
    ElasticSearch flake IDs (which are 20 characters long and map to 15 bytes
    of data).
    """

    impl = postgresql.UUID

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return _get_hex_from_urlsafe(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        hexstring = uuid.UUID(value).hex
        return _get_urlsafe_from_hex(hexstring)


class AnnotationSelectorJSONB(types.TypeDecorator):

    """
    Special type for the Annotation selector column.

    It transparently escapes NULL (\u0000) bytes to \\u0000 when writing to the
    database, and the other way around when reading from the database, but
    only on the prefix/exact/suffix fields in a TextQuoteSelector.
    """

    impl = postgresql.JSONB

    def process_bind_param(self, value, dialect):
        return _transform_quote_selector(value, _escape_null_byte)

    def process_result_value(self, value, dialect):
        return _transform_quote_selector(value, _unescape_null_byte)


def _get_hex_from_urlsafe(value):
    """
    Convert a URL-safe base 64 ID to a hex UUID.

    :type value: unicode
    :rtype: unicode
    """

    def _fail():
        raise InvalidUUID("{0!r} is not a valid encoded UUID".format(value))

    if not isinstance(value, string_types):
        raise InvalidUUID(
            "`value` is {}, expected one of {}".format(type(value), string_types)
        )

    bytestr = value.encode()

    if len(bytestr) == 22:
        # 22-char inputs represent 16 bytes of data, which when normally
        # base64-encoded would have two bytes of padding on the end, so we add
        # that back before decoding.
        try:
            data = _must_b64_decode(bytestr + b"==", expected_size=16)
        except (TypeError, binascii.Error):
            _fail()
        return binascii.hexlify(data).decode()

    if len(bytestr) == 20:
        # 20-char inputs represent 15 bytes of data, which requires no padding
        # corrections.
        try:
            data = _must_b64_decode(bytestr, expected_size=15)
        except (TypeError, binascii.Error):
            _fail()
        hexstring = binascii.hexlify(data).decode()
        # These are ElasticSearch flake IDs, so to convert them into UUIDs we
        # insert the magic nibbles at the appropriate points. See the comments
        # on ES_FLAKE_MAGIC_BYTE for details.
        return (
            hexstring[0:12]
            + ES_FLAKE_MAGIC_BYTE[0]
            + hexstring[12:15]
            + ES_FLAKE_MAGIC_BYTE[1]
            + hexstring[15:30]
        )

    # Fallthrough: we must have a received a string of invalid length
    _fail()


def _get_urlsafe_from_hex(value):
    """
    Convert a hex UUID to a URL-safe base 64 ID.

    :type value: unicode
    :rtype: unicode
    """

    # Validate and normalise hex string
    hexstring = uuid.UUID(hex=value).hex

    is_flake_id = (
        hexstring[12] == ES_FLAKE_MAGIC_BYTE[0]
        and hexstring[16] == ES_FLAKE_MAGIC_BYTE[1]
    )

    if is_flake_id:
        # The hex representation of the flake ID is simply the UUID without the
        # two magic nibbles.
        data = binascii.unhexlify(hexstring[0:12] + hexstring[13:16] + hexstring[17:32])
        return base64.urlsafe_b64encode(data).decode()

    # Encode UUID bytes and strip two bytes of padding
    data = binascii.unhexlify(hexstring)
    return base64.urlsafe_b64encode(data)[:-2].decode()


def _must_b64_decode(data, expected_size=None):
    result = base64.urlsafe_b64decode(data)
    if expected_size is not None and len(result) != expected_size:
        raise TypeError("incorrect data size")
    return result


def _transform_quote_selector(selectors, transform_func):
    if selectors is None:
        return None

    if not isinstance(selectors, list):
        return selectors

    for selector in selectors:
        if not isinstance(selector, dict):
            continue

        if not selector.get("type") == "TextQuoteSelector":
            continue

        if "prefix" in selector:
            selector["prefix"] = transform_func(selector["prefix"])
        if "exact" in selector:
            selector["exact"] = transform_func(selector["exact"])
        if "suffix" in selector:
            selector["suffix"] = transform_func(selector["suffix"])

    return selectors


def _escape_null_byte(s):
    if s is None:
        return s

    return s.replace("\u0000", "\\u0000")


def _unescape_null_byte(s):
    if s is None:
        return s

    return s.replace("\\u0000", "\u0000")
