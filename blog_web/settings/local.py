from blog_web.settings._debug_toolbar import *
from blog_web.settings.base import *
from blog_web.settings.utils import get_logger_config

DEBUG = True
INTERNAL_IPS = ['127.0.0.1']
ALLOWED_HOSTS = ['*']

LMS_SEGMENT_KEY = None
LMS_ROOT_URL = "http://localhost:8181"

# CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        #"KEY_FUNCTION": "course_discovery.apps.core.utils.safe_key",
        "KEY_PREFIX": "default",
        "LOCATION": [
            "127.0.0.1:11211"
        ],
        "VERSION": "1"
    }
}
# END CACHE CONFIGURATION

# DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xblog',
        'USER': 'root',
        'PASSWORD': 'Kevin-2018',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
# END DATABASE CONFIGURATION

# EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# END EMAIL CONFIGURATION

# AUTHENTICATION
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

# Set these to the correct values for your OAuth2/OpenID Connect provider (e.g., devstack)
OAUTH2_PROVIDER_URL = 'http://127.0.0.1:8000/oauth2'
SOCIAL_AUTH_EDX_OIDC_KEY = 'credentials-key'
SOCIAL_AUTH_EDX_OIDC_SECRET = 'credentials-secret'
SOCIAL_AUTH_EDX_OIDC_URL_ROOT = OAUTH2_PROVIDER_URL
SOCIAL_AUTH_EDX_OIDC_ID_TOKEN_DECRYPTION_KEY = SOCIAL_AUTH_EDX_OIDC_SECRET

ENABLE_AUTO_AUTH = False

# CATALOG API CONFIGURATION
# Specified in seconds. Enable caching by setting this to a value greater than 0.
PROGRAMS_CACHE_TTL = 60

# USER API CONFIGURATION
# Specified in seconds. Enable caching by setting this to a value greater than 0.
USER_CACHE_TTL = 60

# LOGGING
LOGGING = get_logger_config(debug=DEBUG, dev_env=True, local_loglevel='DEBUG')

#EDX_CREDENTIALS_NAME = 'edx/credentials'
#STATIC_URL = '/' + EDX_CREDENTIALS_NAME + STATIC_URL
#STATIC_ROOT = '/edx/var/credentials/staticfiles'
#MEDIA_URL = '/' + EDX_CREDENTIALS_NAME + MEDIA_URL
#MEDIA_ROOT = '/edx/var/credentials/media'

JWT_AUTH.update({
    'JWT_SECRET_KEY': 'lms-secret',
    'JWT_ISSUER': 'https://elearningx.test.huawei.com/oauth2',
    'JWT_AUDIENCE': 'lms-key',
    'JWT_VERIFY_AUDIENCE': False,
})
# do this after private.py, ensuring this section picks up credential overrides.

#####################################################################
# Lastly, see if the developer has any local overrides.
if os.path.isfile(join(dirname(abspath(__file__)), 'private.py')):
    from .private import *  # pylint: disable=import-error

