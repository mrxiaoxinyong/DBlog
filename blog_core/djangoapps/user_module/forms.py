"""
Utility functions for validating forms
"""
import re
import random
import logging
# from importlib import import_module

from django import forms
# from django.forms import widgets
from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import PasswordResetForm
# from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
# from django.contrib.auth.tokens import default_token_generator
from user_module.models import UserInfo
# from django.utils.http import int_to_base36
from django.utils.translation import ugettext_lazy as _
# from django.template import loader
from user_module.utils import  validate_password_strength
from django.core.validators import RegexValidator

from django.conf import settings

_USERNAME_TOO_SHORT_MSG = _("Username must be minimum of two characters long")
_EMAIL_INVALID_MSG = _("A properly formatted e-mail is required")
_PASSWORD_INVALID_MSG = _("A valid password is required")
_NAME_TOO_SHORT_MSG = _("Your legal name must be a minimum of two characters long")
_PHONE_INVALID_MSG = _("A valid phone number is required")
_PHONE_REQUIRED_MSG = _('An account with this phone number already exists.')
_PHONE_TOO_LONG_MSG = _("Phone number must be maximum of 25 characters long.")
_NICK_NAME_INVALID_MSG = _("A valid nick name is required")
_NICKNAME_TOO_LONG_MSG = _("Nick name must be maximum of 25 characters long")
_CONFIRM_PASSWORD_ERROR = _("Confirmation password is not identical")
_CONFIRM_PASSWORD_REQUIRED = _("You must enter and confirm your new password.")
slug_re = re.compile(r'^[-a-zA-Z0-9_.]+\Z')

validate_slug = RegexValidator(slug_re,
    u"Enter a valid 'slug' consisting of letters, numbers, underscores, "
    u"dots or hyphens.", 'invalid')


class MySlugField(forms.SlugField):
    """A custom field where dots *are* allowed in the slug.
    This is needed for backwards compatibility with my Plone weblog items.
    """
    default_error_messages = {
        'invalid': u"Enter a valid 'slug' consisting of letters, numbers, "
                   u"underscores, dots or hyphens.",
    }
    default_validators = [validate_slug]


class AccountCreationForm(forms.Form):
    """
    A form to for account creation data. It is currently only used for
    validation, not rendering.
    """
    # TODO: Resolve repetition
    # username = forms.SlugField(
    username = MySlugField(
        required=True,
        min_length=2,
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-username form-control", "placeholder": "Username...",
                                          "id": "form-username", "name": "form-username"}),
        label="用户名",
        error_messages={
            "required": _USERNAME_TOO_SHORT_MSG,
            "invalid": _("Public Username can only contain Roman letters, western numerals (0-9), underscores (_), and "
                         "hyphens (-)."),
            "min_length": _USERNAME_TOO_SHORT_MSG,
            "max_length": _("Username cannot be more than %(limit_value)s characters long"),
        }
    )
    password = forms.CharField(
        required=True,
        min_length=2,
        widget=forms.PasswordInput(attrs={"name": "form-password", "placeholder": "Password...",
                                      "class": "form-password form-control", "id": "form-password"}),
        label="密码",
        error_messages={
            "required": _PASSWORD_INVALID_MSG,
            "min_length": _PASSWORD_INVALID_MSG,
        }
    )
    confirm_password = forms.CharField(
        required=True,
        min_length=2,
        widget=forms.PasswordInput(attrs={"name": "form-password", "placeholder": "Confirm Password...",
                                      "class": "form-password form-control", "id": "form-password"}),
        label="确认密码",
        error_messages={
            "required": _PASSWORD_INVALID_MSG,
            "min_length": _PASSWORD_INVALID_MSG,
        }
    )
    email = forms.EmailField(
        required=True,
        max_length=254,  # Limit per RFCs is 254
        widget=forms.TextInput(attrs={"class": "form-username form-control", "placeholder": "Email...",
                                          "id": "form-username", "name": "form-email"}),
        label="邮箱",
        error_messages={
            "required": _EMAIL_INVALID_MSG,
            "invalid": _EMAIL_INVALID_MSG,
            "max_length": _("Email cannot be more than %(limit_value)s characters long"),
        }
    )
    mobile = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-username form-control", "placeholder": "Mobile...",
                                          "id": "form-username", "name": "form-mobile"}),
        label="手机号码",
        error_messages={
            "required": "A properly formatted mobile is required/需要格式正确的电话号>码",
            "invalid": "A properly formatted mobile is required/需要格式正确的电话号码",
        }
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-username form-control", "placeholder": "Full Name...",
                                          "id": "form-username", "name": "form-name"}),
        label="全名",
        min_length=2,
        error_messages={
            "required": _NAME_TOO_SHORT_MSG,
            "min_length": _NAME_TOO_SHORT_MSG,
        }
    )

    image = forms.ImageField(
        required=False
    )

    def __init__(
            self,
            data=None,
            enforce_username_neq_password=False,
            enforce_password_policy=False,
    ):
        super(AccountCreationForm, self).__init__(data)

        self.enforce_username_neq_password = enforce_username_neq_password
        self.enforce_password_policy = enforce_password_policy

    def clean_username(self):
        username = self.cleaned_data["username"]
        if UserInfo.objects.filter(username=username).exists():
                raise ValidationError("用户名已被使用，请换一个试试！！")
        return username

    def clean_mobile_number(self):
        mobile = self.cleaned_data["mobile"]
        # Format Verification of Mobile Phone Numbers
        if mobile:
            if len(mobile) > 25:
                raise ValidationError("Phone number must be maximum of 25 characters long/电话号码必须最大为25个字符长")

            if not mobile.replace('+', '').replace(' ', '').isdigit():
                raise ValidationError(_("A valid phone number is required"))

            if mobile.startswith('+86 '):
                mobile_base = mobile.replace('+86 ', '')
                pattern = '^1[0-9]{10}$'
                regex = re.compile(pattern)
                match = regex.search(mobile_base)
                if not match:
                    raise ValidationError("A valid phone number is required/需要有效>的电话号码")
        return mobile

    def clean_password(self):
        """Enforce password policies (if applicable)"""
        password = self.cleaned_data["password"]
        if (
                "username" in self.cleaned_data and
                self.cleaned_data["username"] == password
        ):
            raise ValidationError(_("Username and password fields cannot match"))
        if self.enforce_password_policy:
            try:
                validate_password_strength(password)
            except (ValidationError, err):
                raise ValidationError(_("Password: ") + "; ".join(err.messages))
        return password

    def clean_confirm_password(self):
        """Comfirm password if exists"""
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password:
            if not confirm_password:
                raise ValidationError(_CONFIRM_PASSWORD_REQUIRED)
            if password != confirm_password:
                raise ValidationError(_CONFIRM_PASSWORD_ERROR)
        return password

    def clean_email(self):
        """ Enforce email restrictions (if applicable) """
        email = self.cleaned_data["email"]
        if not email:
            return None
        email = self.cleaned_data["email"]
        pattern = r'^([\w]+\.*)([\w]+)\@[\w]+\.\w{3}(\.\w{2}|)$'
        if not re.match(pattern, email):
            raise ValidationError(_("A valid email is required"))

        if UserInfo.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                _(
                    "It looks like {email} belongs to an existing account. Try again with a different email address."
                ).format(email=email)
            )
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        # Format Verification of Mobile Phone Numbers
        if phone_number:
            if not settings.FEATURES.get("ALLOW_DUPLICATE_PHONE_NUMBER", False):
                if UserInfo.objects.filter(mobile=phone_number).count() != 0:
                    raise ValidationError(_PHONE_REQUIRED_MSG)

            if len(phone_number) > 25:
                raise ValidationError(_PHONE_TOO_LONG_MSG)

            if not phone_number.replace('+', '').replace(' ', '').isdigit():
                raise ValidationError(_PHONE_INVALID_MSG)

            if phone_number.startswith('+86 '):
                phone = phone_number.replace('+86 ', '')
                pattern = '^1[0-9]{10}$'
                regex = re.compile(pattern)
                match = regex.search(phone)
                if not match:
                    raise ValidationError(_PHONE_INVALID_MSG)
        return phone_number

    def clean_name(self):
        name = self.cleaned_data.get("name")
        username = self.cleaned_data.get('username')
        if name is None:
            return username
        return name

    def clean_image(self):
        """
        Parse year_of_birth to an integer, but just use None instead of raising
        an error if it is malformed
        """
        image_path = self.cleaned_data.get("image")
        if image_path:
            return image_path.strip()
        return None


class LoginForm(forms.Form):
    username = MySlugField(
        required=True,
        min_length=2,
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-username form-control", "placeholder": "Username...",
                                          "id": "form-username", "name": "form-username"}),
        label="用户名",
        error_messages={
            "required": _USERNAME_TOO_SHORT_MSG,
            "invalid": _("Public Username can only contain Roman letters, western numerals (0-9), underscores (_), and "
                         "hyphens (-)."),
            "min_length": _USERNAME_TOO_SHORT_MSG,
            "max_length": _("Username cannot be more than %(limit_value)s characters long"),
        }
    )

    password = forms.CharField(
        required=True,
        min_length=2,
        widget=forms.PasswordInput(attrs={"name": "form-password", "placeholder": "Password...",
                                      "class": "form-password form-control", "id": "form-password"}),
        label="密码",
        error_messages={
            "required": _PASSWORD_INVALID_MSG,
            "min_length": _PASSWORD_INVALID_MSG,
        }
    )

    def __init__(
            self,
            data=None,
            enforce_username_neq_password=False,
            enforce_password_policy=False,
    ):
        super(LoginForm, self).__init__(data)

        self.enforce_username_neq_password = enforce_username_neq_password
        self.enforce_password_policy = enforce_password_policy

    def clean_password(self):
        """Enforce password policies (if applicable)"""
        password = self.cleaned_data["password"]
        if (
                "username" in self.cleaned_data and
                self.cleaned_data["username"] == password
        ):
            raise ValidationError(_("Username and password fields cannot match"))
        if self.enforce_password_policy:
            try:
                validate_password_strength(password)
            except (ValidationError, err):
                raise ValidationError(_("Password: ") + "; ".join(err.messages))
        return password