"""
Module for code that should run during LMS startup
"""

import django
from django.conf import settings
from importlib import import_module

# Force settings to run so that the python path is modified

settings.INSTALLED_APPS  # pylint: disable=pointless-statement

#from openedx.core.lib.django_startup import autostartup
import logging
# import analytics
#from openedx.core.djangoapps.monkey_patch import django_db_models_options

#import xmodule.x_module
#import lms_xblock.runtime

#from startup_configurations.validate_config import validate_lms_config
#from openedx.core.djangoapps.theming.core import enable_theming
#from openedx.core.djangoapps.theming.helpers import is_comprehensive_theming_enabled

#from microsite_configuration import microsite

log = logging.getLogger(__name__)


def run():
    """
    Executed during django startup
    """
    #django_db_models_options.patch()

    # To override the settings before executing the autostartup() for python-social-auth
    #if settings.FEATURES.get('ENABLE_THIRD_PARTY_AUTH', False):
    #    enable_third_party_auth()

    # Comprehensive theming needs to be set up before django startup,
    # because modifying django template paths after startup has no effect.
    #if is_comprehensive_theming_enabled():
    #    enable_theming()

    # We currently use 2 template rendering engines, mako and django_templates,
    # and one of them (django templates), requires the directories be added
    # before the django.setup().
    #microsite.enable_microsites_pre_startup(log)

    django.setup()

    autostartup()

    add_mimetypes()

    # Mako requires the directories to be added after the django setup.
    #microsite.enable_microsites(log)

    # Initialize Segment analytics module by setting the write_key.
    # if settings.LMS_SEGMENT_KEY:
    #     analytics.write_key = settings.LMS_SEGMENT_KEY

    # register any dependency injections that we need to support in edx_proctoring
    # right now edx_proctoring is dependent on the openedx.core.djangoapps.credit
    #if settings.FEATURES.get('ENABLE_SPECIAL_EXAMS'):
    #    # Import these here to avoid circular dependencies of the form:
    #    # edx-platform app --> DRF --> django translation --> edx-platform app
    #    from edx_proctoring.runtime import set_runtime_service
    #    from lms.djangoapps.instructor.services import InstructorService
    #    from openedx.core.djangoapps.credit.services import CreditService
    #    set_runtime_service('credit', CreditService())

        # register InstructorService (for deleting student attempts and user staff access roles)
    #    set_runtime_service('instructor', InstructorService())

    # In order to allow modules to use a handler url, we need to
    # monkey-patch the x_module library.
    # TODO: Remove this code when Runtimes are no longer created by modulestores
    # https://openedx.atlassian.net/wiki/display/PLAT/Convert+from+Storage-centric+runtimes+to+Application-centric+runtimes
    #xmodule.x_module.descriptor_global_handler_url = lms_xblock.runtime.handler_url
    #xmodule.x_module.descriptor_global_local_resource_url = lms_xblock.runtime.local_resource_url

    # validate configurations on startup
    validate_lms_config(settings)


def add_mimetypes():
    """
    Add extra mimetypes. Used in xblock_resource.

    If you add a mimetype here, be sure to also add it in cms/startup.py.
    """
    import mimetypes

    mimetypes.add_type('application/vnd.ms-fontobject', '.eot')
    mimetypes.add_type('application/x-font-opentype', '.otf')
    mimetypes.add_type('application/x-font-ttf', '.ttf')
    mimetypes.add_type('application/font-woff', '.woff')


def enable_microsites():
    """
    Calls the enable_microsites function in the microsite backend.
    Here for backwards compatibility
    """
    microsite.enable_microsites(log)


def enable_third_party_auth():
    """
    Enable the use of third_party_auth, which allows users to sign in to edX
    using other identity providers. For configuration details, see
    common/djangoapps/third_party_auth/settings.py.
    """

    from third_party_auth import settings as auth_settings
    auth_settings.apply_settings(settings)


def validate_lms_config(settings):
    """
    Validates configurations for lms and raise ValueError if not valid
    """
    validate_common_config(settings)

    # validate feature based configurations
    validate_marketing_site_config(settings)

def validate_common_config(settings):
    """
    Validates configurations common for all apps
    """
    if not getattr(settings, 'LMS_ROOT_URL', None):
        raise ValueError("'LMS_ROOT_URL' is not defined.")


def validate_marketing_site_config(settings):
    """
    Validates 'marketing site' related configurations
    """
    #if settings.FEATURES.get('ENABLE_MKTG_SITE'):
    #    if not hasattr(settings, 'MKTG_URLS'):
    #        raise ValueError("'ENABLE_MKTG_SITE' is True, but 'MKTG_URLS' is not defined.")
    #    if not settings.MKTG_URLS.get('ROOT'):
    #        raise ValueError("There is no 'ROOT' defined in 'MKTG_URLS'.")
    pass


def autostartup():
    """
    Execute app.startup:run() for all installed django apps
    """
    for app in settings.INSTALLED_APPS:
        # See if there's a startup module in each app.
        try:
            mod = import_module(app + '.startup')
        except ImportError:
            continue

        # If the module has a run method, run it.
        if hasattr(mod, 'run'):
            mod.run()

