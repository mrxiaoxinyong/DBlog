import logging
from django.shortcuts import render
# from django.contrib.auth.models import User
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

log = logging.getLogger(__name__)



class RegisterView(View):
    form_class = AccountCreationForm
    initial = {'usernmae': 'password'}
    template_name = 'form/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        print(request.POST)
        if not request.POST:
            response_data = {
                "err_msg": _("Parameter cannot be empty"),
                "status": "failed",
                "data": request.POST
            }
            return HttpResponseBadRequest(content=response_data, content_type="application/json")

        form = self.form_class(
            data=request.POST,
            enforce_username_neq_password=True,
            enforce_password_policy=True,
        )
        if not form.is_valid():
            failed_dict = form.errors
            log.error(failed_dict.as_json())
            log.info(failed_dict.values())
            response_data = {
                "err_msg": list(failed_dict.values())[0][0],
                "status": "failed",
                "data": request.POST
            }
            return render(request, self.template_name, {'form': form})
            # return HttpResponseBadRequest(content=list(failed_dict.values())[0][0])
        print(form.cleaned_data)
        user = UserInfo(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            mobile=form.cleaned_data["mobile"],
            real_name=form.cleaned_data["name"],
            is_active=True
        )
        user.set_password(form.cleaned_data["password"])
        user.save()
        return HttpResponseRedirect(reverse("login"))


class LoginView(View):
    form_class = LoginForm
    initial = {'usernmae': 'password'}
    template_name = 'form/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            data=request.POST,
            enforce_username_neq_password=True,
            enforce_password_policy=True,
        )
        if not form.is_valid():
            failed_dict = form.errors
            log.error(failed_dict.as_json())
            log.info(failed_dict.values())
            response_data = {
                "err_msg": list(failed_dict.values())[0][0],
                "status": "failed",
                "data": request.POST
            }
            return render(request, self.template_name, {'form': form})
        user = authenticate(username=form.cleaned_data['username'],
                                 password=form.cleaned_data['password'])
        if user:
            # 用户名和密码正确
            login(request, user)
            redirect_to = get_next_url_for_login_page(request)
            return HttpResponseRedirect(redirect_to)
        else:
            # 密码不正确
            form._errors[NON_FIELD_ERRORS] = form.error_class(['密码错误！！'])
            return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        redirect_to = get_next_url_for_login_page(request)
        return HttpResponseRedirect(redirect_to)


class UserIndexView(View):
    initial = {}
    template_name = 'user/index.html'

    def get(self, request):
        return render(request, self.template_name)



@login_required
def index(request):
    user_obj = request.user
    init_permission(request, user_obj)
    menu_data = get_structure_data(request)
    print(menu_data)
    menu_html = get_menu_html(menu_data)
    print(menu_html)
    return render(request, 'index.html', {"menu_html": menu_html})
    return render(request, 'index.html')


def get_next_url_for_login_page(request):
    """
    Determine the URL to redirect to following login/registration/third_party_auth

    The user is currently on a login or registration page.
    If 'course_id' is set, or other POST_AUTH_PARAMS, we will need to send the user to the
    /account/finish_auth/ view following login, which will take care of auto-enrollment in
    the specified course.

    Otherwise, we go to the ?next= query param or to the dashboard if nothing else is
    specified.
    """
    redirect_to = request.GET.get('next', None)

    # if we get a redirect parameter, make sure it's safe. If it's not, drop the
    # parameter.
    #if redirect_to and not http.is_safe_url(redirect_to):
    login_redirect_whitelist = set()
    if redirect_to and not http.is_safe_url(url=redirect_to, host=request.get_host(),
                                       allowed_hosts=login_redirect_whitelist, require_https=request.is_secure()):
        log.error(
            u'Unsafe redirect parameter detected: %(redirect_to)r',
            {"redirect_to": redirect_to}
        )
        redirect_to = None

    if not redirect_to:
        try:
            redirect_to = reverse('home')
        except Exception:
            redirect_to = reverse('home')
    return redirect_to


    errors = dict()
    if not (data.get('phone_number') or data.get('email')):
        err_msg = _('Please select one of the phone number and email address to complete.')
        errors.update({'username': err_msg})
        raise ValidationError(errors)
    # Captcha handle

    form = AssociateForm(data)
    errors.update(form.errors)
    if errors:
        raise ValidationError(errors)
    # Associate social user
    email = form.cleaned_data.get("email")
    phone_number = form.cleaned_data.get("phone_number")
    try:
        user = User.objects.get(email_iexact=email) if email else UserProfile.objects.get(phone_number=phone_number).user
    except User.DoesNotExist:
        errors.update(_("Email does not exist"))
        raise ValidationError(errors)
    except UserProfile.DoesNotExist:
        errors.update(_("phone number not exist"))
        raise ValidationError(errors)