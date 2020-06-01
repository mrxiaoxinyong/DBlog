from django.utils.translation import ugettext_lazy as _
from djchoices import ChoiceItem, DjangoChoices


class SelectContentChoices(DjangoChoices):
    markdown = ChoiceItem(0, _('markdown'))
    ueditor = ChoiceItem(1, _('ueditor'))


class PublishTypeChoices(DjangoChoices):
    open = ChoiceItem(0, _('open'))
    secret = ChoiceItem(1, _('secret'))
    fans = ChoiceItem(2, _('fans'))
    vip = ChoiceItem(3, _('vip'))
