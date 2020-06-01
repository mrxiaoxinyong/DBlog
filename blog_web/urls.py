"""
URLs for LMS
"""

from django.conf import settings
from django.conf.urls import include, url
# from auth_backends.urls import auth_urlpatterns
from django.views.generic.base import RedirectView
from django.views.i18n import javascript_catalog
from ratelimitbackend import admin
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

#from courseware.views.views import EnrollStaffView
#from config_models.views import ConfigurationModelCurrentAPIView
#from courseware.views.index import CoursewareIndex
#from courseware.views.views import ProgressAPIView, GradesAPIView
#from openedx.core.djangoapps.auth_exchange.views import LoginWithAccessTokenView
#from openedx.core.djangoapps.catalog.models import CatalogIntegration
#from openedx.core.djangoapps.catalog.views import LiveAccessView, LiveAuthView
#from openedx.core.djangoapps.programs.models import ProgramsApiConfig
#from openedx.core.djangoapps.self_paced.models import SelfPacedConfiguration
#from django_comment_common.models import ForumsConfig
#from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
#from util.enterprise_helpers import enterprise_enabled
#from util.views import GetOBSUrlView, GetBannersView, pdf_viewer, check_uniportal_login_by_oauth2, accept_hiclc_login
#
#from video_demand.views import VideoDetail, VideoHlsView, BatchVideoList, CatalogAddVideo
#from video_demand.huaweiVod.views import query_cipher_key
##from progress.views import SubsectionCompletionView
#from mob_upgrade.views import check_mob_upgrade
#from search_record.views import get_user_search_record
from user_module import views
from branding.views import BlogHomeView

# Uncomment the next two lines to enable the admin:
if settings.DEBUG:
    admin.autodiscover()
admin.site.site_header = "博客管理系统"
# Use urlpatterns formatted as within the Django docs with first parameter "stuck" to the open parenthesis
# urlpatterns = auth_urlpatterns + [

urlpatterns = [
    url(r"^home/$",  BlogHomeView.as_view(), name="home"),
    url(r"^register/$",  views.RegisterView.as_view(), name="register"),
    url(r"^login/$",  views.LoginView.as_view(), name="login"),
    url(r"^logout/$",  views.LogoutView.as_view(), name="logout"),
    url(r"^user/", include("user_module.users.urls"), name="user"),
    url(r"^blog/", include("blog_management.urls", namespace="blog")),
    url(r'^ueditor/', include('DjangoUeditor.urls', namespace="ueditor")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    ## Jasmine and admin
    urlpatterns += (url(r'^admin/', include(admin.site.urls)),)

