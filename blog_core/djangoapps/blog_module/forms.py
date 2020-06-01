"""
Utility functions for validating forms
"""
# from importlib import import_module

# from django.forms import widgets
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import PasswordResetForm
# from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import int_to_base36
# from django.template import loader
from blog_module.utils import getImagePath, getUploadPath
from DjangoUeditor.forms import UEditorField
from django import forms


class UeditorForm(forms.Form):
    content_udt = UEditorField(
        label="富文本编辑器", width=922, height=600, toolbars="full",
        imagePath=getImagePath(), filePath=getUploadPath(),
        upload_settings={"imageMaxSize": 1204000}, settings={})


class CatalogForm(forms.Form):
    name = forms.CharField(label="标题",
                           required=True,
                           widget=forms.TextInput(
                               attrs={"class": "layui-input", "placeholder": "标题...","name": "title"}),
                           error_messages={
                               "required": "title is required/标题不能为空",
                           }
                           )

    describe = forms.CharField(label="描述",
                               required=False,
                               widget=forms.Textarea(
                                   attrs={"placeholder": "描述...", "class": "layui-textarea",
                                          "name": "form-describe"}),
                               )

    image = forms.ImageField(label="配图",
                             required=False,
                             widget=forms.FileInput(
                                 attrs={"name": "配图", "id": "chooseImage", "class": "hidden", "accept": ".jpg,.jpeg,.png"}
                             )
                             )
