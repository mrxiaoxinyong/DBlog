"""
This file exposes a number of password complexity validators which can be optionally added to
account creation

This file was inspired by the django-passwords project at https://github.com/dstufft/django-passwords
authored by dstufft (https://github.com/dstufft)
"""
from __future__ import division
import string
import unicodedata

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.password_validation import (
    get_default_password_validators,
    validate_password as django_validate_password,
    MinimumLengthValidator as DjangoMinimumLengthValidator,
)

import nltk


def validate_password_strength(value):
    """
    This function loops through each validator defined in this file
    and applies it to a user's proposed password

    Args:
        value: a user's proposed password

    Returns: None, but raises a ValidationError if the proposed password
        fails any one of the validators in password_validators
    """
    password_validators = [
        validate_password_length,
        validate_password_complexity,
        validate_password_dictionary,
    ]
    for validator in password_validators:
        validator(value)


def validate_password_length(value):
    """
    Validator that enforces minimum length of a password
    """
    message = _("Invalid Length ({0})")
    code = "length"

    min_length = getattr(settings, 'PASSWORD_MIN_LENGTH', None)
    max_length = getattr(settings, 'PASSWORD_MAX_LENGTH', None)

    min_length_error = True if min_length and len(value) < min_length else False
    max_length_error = True if max_length and len(value) > max_length else False

    if min_length_error or max_length_error:
        raise ValidationError(message.format(_("must between {0}-{1} characters").format(min_length, max_length)),
                              code=code)
    # if min_length and len(value) < min_length:
    #    raise ValidationError(message.format(_("must be {0} characters or more").format(min_length)), code=code)
    # elif max_length and len(value) > max_length:
    #    raise ValidationError(message.format(_("must be {0} characters or fewer").format(max_length)), code=code)


def validate_password_complexity(value):
    """
    Validator that enforces minimum complexity
    """
    message = _("Must be more complex ({0})")
    code = "complexity"

    complexities = getattr(settings, "PASSWORD_COMPLEXITY", None)

    if complexities is None:
        return

    uppercase, lowercase, digits, non_ascii, punctuation = set(), set(), set(), set(), set()

    for character in value:
        if character.isupper():
            uppercase.add(character)
        elif character.islower():
            lowercase.add(character)
        elif character.isdigit():
            digits.add(character)
        elif character in string.punctuation:
            punctuation.add(character)
        else:
            non_ascii.add(character)

    words = set(value.split())

    errors = []
    alpha_length = len(uppercase) + len(lowercase)
    if alpha_length < complexities.get("ALPHA", 0):
        errors.append(_("must contain {0} or more alpha characters").format(complexities["ALPHA"]))
    if len(uppercase) < complexities.get("UPPER", 0):
        errors.append(_("must contain {0} or more uppercase characters").format(complexities["UPPER"]))
    if len(lowercase) < complexities.get("LOWER", 0):
        errors.append(_("must contain {0} or more lowercase characters").format(complexities["LOWER"]))
    if len(digits) < complexities.get("DIGITS", 0):
        errors.append(_("must contain {0} or more digits").format(complexities["DIGITS"]))
    if len(punctuation) < complexities.get("PUNCTUATION", 0):
        errors.append(_("must contain {0} or more punctuation characters").format(complexities["PUNCTUATION"]))
    if len(non_ascii) < complexities.get("NON ASCII", 0):
        errors.append(_("must contain {0} or more non ascii characters").format(complexities["NON ASCII"]))
    if len(words) < complexities.get("WORDS", 0):
        errors.append(_("must contain {0} or more unique words").format(complexities["WORDS"]))

    if errors:
        raise ValidationError(message.format(u', '.join(errors)), code=code)


def validate_password_dictionary(value):
    """
    Insures that the password is not too similar to a defined set of dictionary words
    """
    password_max_edit_distance = getattr(settings, "PASSWORD_DICTIONARY_EDIT_DISTANCE_THRESHOLD", None)
    password_dictionary = getattr(settings, "PASSWORD_DICTIONARY", None)

    if password_max_edit_distance and password_dictionary:
        for word in password_dictionary:
            distance = nltk.metrics.distance.edit_distance(value, word)
            if distance <= password_max_edit_distance:
                raise ValidationError(_("Too similar to a restricted dictionary word."), code="dictionary_word")


def normalize_password(password):
    """
    Converts the password to utf-8 if it is not unicode already.
    Normalize all passwords to 'NFKC' across the platform to prevent mismatched hash strings when comparing entered
    passwords on login. See LEARNER-4283 for more context.
    """
    if not isinstance(password, text_type):
        try:
            # some checks rely on unicode semantics (e.g. length)
            password = text_type(password, encoding='utf8')
        except UnicodeDecodeError:
            # no reason to get into weeds
            raise ValidationError([_('Invalid password.')])
    return unicodedata.normalize('NFKC', password)


def validate_password(password, user=None):
    """
    EdX's custom password validator for passwords. This function performs the
    following functions:
        1) Normalizes the password according to NFKC unicode standard
        2) Calls Django's validate_password method. This calls the validate function
            in all validators specified in AUTH_PASSWORD_VALIDATORS configuration.

    Parameters:
        password (str or unicode): the user's password to be validated
        user (django.contrib.auth.models.User): The user object to use for validating
        the given password against the username and/or email.

    Returns:
        None

    Raises:
        ValidationError if any of the password validators fail.
    """
    password = normalize_password(password)
    django_validate_password(password, user)