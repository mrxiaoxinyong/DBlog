import logging
from django.shortcuts import render
from user_module.models import UserInfo
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST, require_http_methods
from django.core import serializers
from django.urls import reverse
from permission_module.utils import init_permission, get_structure_data, get_menu_html
from django.shortcuts import HttpResponseRedirect
from user_module.forms import AccountCreationForm, LoginForm
from django.http import (
    HttpResponse,
    JsonResponse,
    Http404,
    HttpResponseForbidden,
    HttpResponseBadRequest,
    HttpResponseRedirect
)
from django.forms.forms import NON_FIELD_ERRORS
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login
from django.views.generic.base import View
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import http
from blog_module.models import (
    PublishArticle,
    UserCatagory, Label
)

log = logging.getLogger(__name__)


class BlogHomeView(View):
    initial = {}
    template_name = 'home.html'

    def get(self, request):
        context = {
            "username": request.user.username,
            "articles": PublishArticle.objects.all()
        }
        return render(request, self.template_name, context)
