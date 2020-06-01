import base64
import imghdr
import logging
from io import BytesIO

from blog_module.forms import UeditorForm, CatalogForm
from blog_module.models import (
    PublishArticle,
    UserCatagory, Label
)
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.utils import IntegrityError
from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect
)
from django.shortcuts import render
# from django.utils.decorators import method_decorator
# from user_module.models import UserInfo
# from django.utils.translation import ugettext as _
# from django.views.decorators.http import require_POST, require_http_methods
# from django.core import serializers
from django.urls import reverse
from django.utils.decorators import method_decorator
# from permission_module.utils import init_permission, get_structure_data, get_menu_html
# from django.shortcuts import HttpResponseRedirect
# from user_module.forms import AccountCreationForm, LoginForm
# from django.http import (
#     HttpResponse,
#     JsonResponse,
#     Http404,
#     HttpResponseForbidden,
#     HttpResponseBadRequest,
#     HttpResponseRedirect
# )
# from django.forms.forms import NON_FIELD_ERRORS
# from django.views.decorators.csrf import ensure_csrf_cookie
# from django.contrib.auth import authenticate, login
# from django.contrib.auth import logout
# from django.utils import http
from django.views.generic.base import View
from rest_framework import authentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

log = logging.getLogger(__name__)
IMAGE_DEFAULT = "/static/blog/images/icon/noimg.gif"


class BlogManageView(View):
    initial = {}
    template_name = 'blog/index.html'

    @method_decorator(login_required)
    def get(self, request):
        articles = PublishArticle.objects.all()
        context = {
            "username": request.user.username,
            "articles": articles
        }
        return render(request, self.template_name, context)


class BlogDetailView(View):
    initial = {}
    template_name = 'blog/show.html'

    @method_decorator(login_required)
    def get(self, request, article_id):
        article = PublishArticle.objects.get(uuid=article_id)
        context = {
            "username": request.user.username,
            "article": article
        }
        return render(request, self.template_name, context)


class BlogEditView(View):
    initial = {}
    template_name = 'blog/release.html'

    @method_decorator(login_required)
    def get(self, request):
        form = UeditorForm()
        user_catalog = UserCatagory.objects.all()
        label = Label.objects.all()
        context = {
            "username": request.user.username,
            "form": form,
            "user_catalog": user_catalog,
            'label': label
        }
        return render(request, self.template_name, context)


class BlogEditMarkdownView(View):
    initial = {}
    template_name = 'blog/markdown.html'

    @method_decorator(login_required)
    def get(self, request):
        context = {
            "username": request.user.username
        }
        return render(request, self.template_name, context)


class CatalogEditView(View):
    form_class = CatalogForm
    initial = {}
    template_name = 'blog/related.html'

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class()
        context = {
            "username": request.user.username,
            "form": form
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = self.form_class(
            data=request.POST,
        )
        if not form.is_valid():
            failed_dict = form.errors
            return HttpResponseBadRequest(content=list(failed_dict.values())[0][0])

        if request.POST.get("image") and request.POST.get("image") != IMAGE_DEFAULT:
            try:
                image = base64.b64decode(request.POST.get("image").split(';base64,')[1])
            except Exception:
                return HttpResponseBadRequest(content="图片格式有问题！！")

            s = imghdr.what(None, image)
            print(s)
            f = BytesIO()
            f.write(image)
            image = InMemoryUploadedFile(f, "test", 'png', None, len(image), None, None)
        else:
            image = None
        print(image)
        try:
            user_catalog = UserCatagory.objects.create(
                author=request.user,
                name=request.POST.get("name"),
                describe=request.POST.get("describe"),
                image=image
            )
        except IntegrityError:
            return HttpResponseBadRequest(content="该标签你已经使用！！")
        response_data = {
            "err_msg": None,
            "status": "completed",
            "name": user_catalog.name,
            "id": user_catalog.id
        }
        return JsonResponse(data=response_data)


class BlogArticleView(GenericViewSet):
    authentication_classes = (
        authentication.SessionAuthentication,
    )
    permission_classes = (IsAuthenticated,)
    lookup_field = 'article_uuid'

    def list(self, request):
        full_name = request.query_params.get("full_name")
        email = request.query_params.get("email")
        mobile = request.query_params.get("mobile")
        pass

    def retrieve(self, request, article_uuid):
        pass

    def create(self, request, *args, **kwargs):
        data = request.data
        response_data = {
            "err_msg": "Parameter Error",
            "status": "failed",
            "data": request.data
        }
        try:

            label = Label.objects.get(id=request.data.get("label_id"))
            category = UserCatagory.objects.get(id=request.data.get("category_id"))
        except (Label.DoesNotExist, UserCatagory.DoesNotExist):
            return Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.data.get("content_mkd"):
            select_content = 0
        else:
            select_content = 1

        if request.data.get("image") and request.data.get("image") != IMAGE_DEFAULT:
            try:
                image = base64.b64decode(request.data.get("image").split(';base64,')[1])
            except Exception:
                return Response(
                    data=response_data,
                    status=status.HTTP_400_BAD_REQUEST
                )

            s = imghdr.what(None, image)
            print(s)
            f = BytesIO()
            f.write(image)
            image = InMemoryUploadedFile(f, "test", 'png', None, len(image), None, None)
        else:
            image = None

        if data.get("version"):
            publish_article = PublishArticle.objects.create(
                author=request.user,
                category=category,
                title=request.data.get("title"),
                content_mkd=request.data.get("content_mkd"),
                content_udt=request.data.get("content_udt"),
                select_content=select_content,
                publish_type=request.data.get("publish_type") if request.data.get("publish_type") else 1,
                image=image
            )
            publish_article.label.add(label)
        response_data = {
            "err_msg": None,
            "status": "completed",
            "data": request.data
        }
        return Response(
            data=response_data,
            status=status.HTTP_200_OK
        )
