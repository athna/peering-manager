# DO NOT EDIT THIS FILE!
#
# All configuration must be done in the `configuration.py` file.
# This file is part of the Peering Manager code and it will be overwritten with
# every code releases.


import contextlib
import hashlib
import importlib
import os
import platform
import sys
import warnings
from importlib.util import find_spec
from pathlib import Path

import requests
from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.validators import URLValidator

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
HOSTNAME = platform.node()
BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"

VERSION = "1.9.5-dev"

major, minor, _ = platform.python_version_tuple()
if (int(major), int(minor)) < (3, 10):
    raise RuntimeError(
        f"Peering Manager requires Python 3.10 or higher (current: Python {platform.python_version()})"
    )

# Import configuration parameters
config_path = os.getenv("PEERINGMANAGER_CONFIGURATION", "peering_manager.configuration")
try:
    configuration = importlib.import_module(config_path)
except ModuleNotFoundError as e:
    if e.name == config_path:
        raise ImproperlyConfigured(
            f"Specified configuration module ({config_path}) not found. Please define peering_manager/configuration.py per the documentation, or specify an alternate module in the PEERINGMANAGER_CONFIGURATION environment variable."
        ) from e
    raise

for setting in ["ALLOWED_HOSTS", "DATABASE", "SECRET_KEY"]:
    if not hasattr(configuration, setting):
        raise ImproperlyConfigured(
            f"Mandatory setting {setting} is not in the configuration.py file."
        )

# Set required parameters
ALLOWED_HOSTS = configuration.ALLOWED_HOSTS
DATABASE = configuration.DATABASE
SECRET_KEY = configuration.SECRET_KEY

# Deprecated, to be removed in 2.0.0
MY_ASN = getattr(configuration, "MY_ASN", None)
if MY_ASN:
    warnings.warn(
        "MY_ASN is no longer supported and will be removed in 2.0.", stacklevel=1
    )

BASE_PATH = getattr(configuration, "BASE_PATH", "")
if BASE_PATH:
    BASE_PATH = BASE_PATH.strip("/") + "/"  # Enforce trailing slash only
CENSUS_REPORTING_ENABLED = getattr(configuration, "CENSUS_REPORTING_ENABLED", True)
CSRF_COOKIE_PATH = LANGUAGE_COOKIE_PATH = SESSION_COOKIE_PATH = (
    f"/{BASE_PATH.rstrip('/')}"
)
CORS_ORIGIN_ALLOW_ALL = getattr(configuration, "CORS_ORIGIN_ALLOW_ALL", False)
CORS_ORIGIN_REGEX_WHITELIST = getattr(configuration, "CORS_ORIGIN_REGEX_WHITELIST", [])
CORS_ORIGIN_WHITELIST = getattr(configuration, "CORS_ORIGIN_WHITELIST", [])
CSRF_COOKIE_NAME = getattr(configuration, "CSRF_COOKIE_NAME", "csrftoken")
CSRF_COOKIE_SECURE = getattr(configuration, "CSRF_COOKIE_SECURE", False)
CSRF_TRUSTED_ORIGINS = getattr(configuration, "CSRF_TRUSTED_ORIGINS", [])
DEBUG = getattr(configuration, "DEBUG", False)
LOGGING = getattr(configuration, "LOGGING", {})
REDIS = getattr(configuration, "REDIS", {})
RQ_DEFAULT_TIMEOUT = getattr(configuration, "RQ_DEFAULT_TIMEOUT", 300)
CACHE_BGP_DETAIL_TIMEOUT = getattr(configuration, "CACHE_BGP_DETAIL_TIMEOUT", 900)
CHANGELOG_RETENTION = getattr(configuration, "CHANGELOG_RETENTION", 90)
JOB_RETENTION = getattr(configuration, "JOB_RETENTION", 90)
LOGIN_PERSISTENCE = getattr(configuration, "LOGIN_PERSISTENCE", False)
LOGIN_REQUIRED = getattr(configuration, "LOGIN_REQUIRED", False)
LOGIN_TIMEOUT = getattr(configuration, "LOGIN_TIMEOUT", None)
BANNER_LOGIN = getattr(configuration, "BANNER_LOGIN", "")
NAPALM_USERNAME = getattr(configuration, "NAPALM_USERNAME", "")
NAPALM_PASSWORD = getattr(configuration, "NAPALM_PASSWORD", "")
NAPALM_TIMEOUT = getattr(configuration, "NAPALM_TIMEOUT", 30)
NAPALM_ARGS = getattr(configuration, "NAPALM_ARGS", {})
PAGINATE_COUNT = getattr(configuration, "PAGINATE_COUNT", 20)
MAX_PAGE_SIZE = getattr(configuration, "MAX_PAGE_SIZE", 1000)
DEFAULT_USER_PREFERENCES = getattr(configuration, "DEFAULT_USER_PREFERENCES", {})
METRICS_ENABLED = getattr(configuration, "METRICS_ENABLED", False)

SESSION_FILE_PATH = getattr(configuration, "SESSION_FILE_PATH", None)
SESSION_COOKIE_NAME = getattr(configuration, "SESSION_COOKIE_NAME", "sessionid")
SESSION_COOKIE_SECURE = getattr(configuration, "SESSION_COOKIE_SECURE", False)

REMOTE_AUTH_ENABLED = getattr(configuration, "REMOTE_AUTH_ENABLED", False)
REMOTE_AUTH_AUTO_CREATE_GROUPS = getattr(
    configuration, "REMOTE_AUTH_AUTO_CREATE_GROUPS", False
)
REMOTE_AUTH_AUTO_CREATE_USER = getattr(
    configuration, "REMOTE_AUTH_AUTO_CREATE_USER", False
)
REMOTE_AUTH_BACKEND = getattr(
    configuration,
    "REMOTE_AUTH_BACKEND",
    "peering_manager.authentication.RemoteUserBackend",
)
REMOTE_AUTH_DEFAULT_GROUPS = getattr(configuration, "REMOTE_AUTH_DEFAULT_GROUPS", [])
REMOTE_AUTH_DEFAULT_PERMISSIONS = getattr(
    configuration, "REMOTE_AUTH_DEFAULT_PERMISSIONS", []
)
REMOTE_AUTH_GROUP_HEADER = getattr(
    configuration, "REMOTE_AUTH_GROUP_HEADER", "HTTP_REMOTE_USER_GROUP"
)
REMOTE_AUTH_GROUP_SEPARATOR = getattr(configuration, "REMOTE_AUTH_GROUP_SEPARATOR", "|")
REMOTE_AUTH_GROUP_SYNC_ENABLED = getattr(
    configuration, "REMOTE_AUTH_GROUP_SYNC_ENABLED", False
)
REMOTE_AUTH_HEADER = getattr(configuration, "REMOTE_AUTH_HEADER", "HTTP_REMOTE_USER")
REMOTE_AUTH_SUPERUSER_GROUPS = getattr(
    configuration, "REMOTE_AUTH_SUPERUSER_GROUPS", []
)
REMOTE_AUTH_SUPERUSERS = getattr(configuration, "REMOTE_AUTH_SUPERUSERS", [])
REMOTE_AUTH_USER_EMAIL = getattr(
    configuration, "REMOTE_AUTH_USER_EMAIL", "HTTP_REMOTE_USER_EMAIL"
)
REMOTE_AUTH_USER_FIRST_NAME = getattr(
    configuration, "REMOTE_AUTH_USER_FIRST_NAME", "HTTP_REMOTE_USER_FIRST_NAME"
)
REMOTE_AUTH_USER_LAST_NAME = getattr(
    configuration, "REMOTE_AUTH_USER_LAST_NAME", "HTTP_REMOTE_USER_LAST_NAME"
)
REMOTE_AUTH_STAFF_GROUPS = getattr(configuration, "REMOTE_AUTH_STAFF_GROUPS", [])
REMOTE_AUTH_STAFF_USERS = getattr(configuration, "REMOTE_AUTH_STAFF_USERS", [])

DATE_FORMAT = getattr(configuration, "DATE_FORMAT", "jS F, Y")
DATETIME_FORMAT = getattr(configuration, "DATETIME_FORMAT", "jS F, Y G:i")
SHORT_DATE_FORMAT = getattr(configuration, "SHORT_DATE_FORMAT", "Y-m-d")
SHORT_DATETIME_FORMAT = getattr(configuration, "SHORT_DATETIME_FORMAT", "Y-m-d H:i")
SHORT_TIME_FORMAT = getattr(configuration, "SHORT_TIME_FORMAT", "H:i:s")
TIME_FORMAT = getattr(configuration, "TIME_FORMAT", "G:i")
try:
    with Path("/etc/timezone").open() as f:
        BASE_TZ = f.readline()

    # For some reasons, Django does not seem to be happy about this particular value
    if "Etc/UTC" in BASE_TZ:
        raise Exception("Unsupported TZ")
except (OSError, Exception):
    BASE_TZ = "UTC"
TIME_ZONE = getattr(configuration, "TIME_ZONE", BASE_TZ).rstrip()

EMAIL = getattr(configuration, "EMAIL", {})
HTTP_PROXIES = getattr(configuration, "HTTP_PROXIES", None)
BGPQ3_PATH = getattr(configuration, "BGPQ3_PATH", "bgpq3")
BGPQ3_HOST = getattr(configuration, "BGPQ3_HOST", "rr.ntt.net")
BGPQ3_SOURCES = getattr(
    configuration,
    "BGPQ3_SOURCES",
    "RPKI,RIPE,ARIN,APNIC,AFRINIC,LACNIC,RIPE-NONAUTH,RADB,ALTDB,NTTCOM,LEVEL3,TC",
)
BGPQ3_ARGS = getattr(
    configuration,
    "BGPQ3_ARGS",
    {"ipv6": ["-r", "16", "-R", "48"], "ipv4": ["-r", "8", "-R", "24"]},
)
JINJA2_TEMPLATE_EXTENSIONS = getattr(configuration, "JINJA2_TEMPLATE_EXTENSIONS", [])
CONFIG_CONTEXT_MERGE_STRATEGY = {
    "recursive": getattr(configuration, "CONFIG_CONTEXT_RECURSIVE_MERGE", True),
    "list_merge": getattr(configuration, "CONFIG_CONTEXT_LIST_MERGE", "replace"),
}
GIT_COMMIT_AUTHOR = getattr(
    configuration, "GIT_COMMIT_AUTHOR", "Peering Manager <no-reply@peering-manager.net>"
)
GIT_COMMIT_MESSAGE = getattr(
    configuration, "GIT_COMMIT_MESSAGE", "Committed using Peering Manager"
)
VALIDATE_BGP_COMMUNITY_VALUE = getattr(
    configuration, "VALIDATE_BGP_COMMUNITY_VALUE", True
)

# Django filters
FILTERS_NULL_CHOICE_LABEL = "-- None --"
FILTERS_NULL_CHOICE_VALUE = "null"


# Use major.minor as API version
REST_FRAMEWORK_VERSION = ".".join(VERSION.split("-")[0].split(".")[:2])
REST_FRAMEWORK = {
    "ALLOWED_VERSIONS": [REST_FRAMEWORK_VERSION],
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "peering_manager.api.authentication.TokenAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_METADATA_CLASS": "peering_manager.api.metadata.BulkOperationMetadata",
    "DEFAULT_PAGINATION_CLASS": "peering_manager.api.pagination.OptionalLimitOffsetPagination",
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "peering_manager.api.authentication.TokenPermissions",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "peering_manager.api.renderers.FormlessBrowsableAPIRenderer",
    ),
    "DEFAULT_SCHEMA_CLASS": "core.api.schema.PeeringManagerAutoSchema",
    "DEFAULT_VERSION": REST_FRAMEWORK_VERSION,
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.AcceptHeaderVersioning",
    "SCHEMA_COERCE_METHOD_NAMES": {
        # Default mappings
        "retrieve": "read",
        "destroy": "delete",
        # Custom operations
        "bulk_destroy": "bulk_delete",
    },
    "VIEW_NAME_FUNCTION": "utils.api.get_view_name",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Peering Manager API",
    "DESCRIPTION": "API to access Peering Manager data",
    "LICENSE": {"name": "Apache v2 License"},
    "VERSION": VERSION,
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "POSTPROCESSING_HOOKS": [],
}


# Case insensitive search for tags
TAGGIT_CASE_INSENSITIVE = True


# User-Agent for requests
REQUESTS_USER_AGENT = getattr(
    configuration, "REQUESTS_USER_AGENT", f"PeeringManager/{VERSION[0:3]}"
)


# NetBox API configuration
NETBOX_API = getattr(configuration, "NETBOX_API", "")
NETBOX_URL = NETBOX_API.strip("/")
if NETBOX_URL.endswith("/api"):
    NETBOX_URL = NETBOX_URL[:-3]
NETBOX_API_TOKEN = getattr(configuration, "NETBOX_API_TOKEN", "")
NETBOX_API_THREADING = getattr(configuration, "NETBOX_API_THREADING", False)
NETBOX_API_VERIFY_SSL = getattr(configuration, "NETBOX_API_VERIFY_SSL", True)
NETBOX_DEVICE_ROLES = getattr(
    configuration, "NETBOX_DEVICE_ROLES", ["router", "firewall"]
)
# TODO: Defaults to ["peering-manager"] as of next major release
NETBOX_TAGS = set(getattr(configuration, "NETBOX_TAGS", []))

# PeeringDB URLs
PEERINGDB = "https://www.peeringdb.com/"
PEERINGDB_API = f"{PEERINGDB}api/"
PEERINGDB_ASN = f"{PEERINGDB}asn/"
# To be removed in v2.0
PEERINGDB_USERNAME = getattr(configuration, "PEERINGDB_USERNAME", "")
PEERINGDB_PASSWORD = getattr(configuration, "PEERINGDB_PASSWORD", "")
if PEERINGDB_USERNAME or PEERINGDB_PASSWORD:
    warnings.warn(
        "PEERINGDB_USERNAME and PEERINGDB_PASSWORD are deprecated and will be removed in 2.0. Use PEERINGDB_API_KEY instead.",
        stacklevel=1,
    )
PEERINGDB_API_KEY = getattr(configuration, "PEERINGDB_API_KEY", "")

# GitHub releases check
RELEASE_CHECK_URL = getattr(
    configuration,
    "RELEASE_CHECK_URL",
    "https://api.github.com/repos/peering-manager/peering-manager/releases",
)

# Validate repository URL and timeout
if RELEASE_CHECK_URL:
    try:
        URLValidator(RELEASE_CHECK_URL)
    except ValidationError as e:
        raise ImproperlyConfigured(
            "RELEASE_CHECK_URL must be a valid API URL. "
            "Example: https://api.github.com/repos/peering-manager/peering-manager"
        ) from e

# Set up authentication backends
if not isinstance(REMOTE_AUTH_BACKEND, list | tuple):
    REMOTE_AUTH_BACKEND = [REMOTE_AUTH_BACKEND]
AUTHENTICATION_BACKENDS = [
    *REMOTE_AUTH_BACKEND,
    "peering_manager.authentication.ModelBackend",
]

# If RADIUS auth has been configured, make sure it can be used
if "radiusauth.backends.RADIUSBackend" in AUTHENTICATION_BACKENDS:
    if find_spec("radiusauth") is None:
        raise ImproperlyConfigured(
            "RADIUS authentication has been configured, but django-radius is not installed."
        )
    try:
        from peering_manager.radius_config import *  # type: ignore
    except ModuleNotFoundError as e:
        raise ImproperlyConfigured(
            "LDAP configuration file not found: Check that radius_config.py has been created alongside configuration.py."
        ) from e


# Force PostgreSQL to be used as database backend
configuration.DATABASE.update({"ENGINE": "django.db.backends.postgresql"})
# Actually set the database's settings
DATABASES = {"default": configuration.DATABASE}


# Redis
# Background task queuing
if "tasks" not in REDIS:
    raise ImproperlyConfigured(
        "REDIS section in configuration.py is missing the 'tasks' subsection."
    )
TASKS_REDIS = REDIS["tasks"]
TASKS_REDIS_HOST = TASKS_REDIS.get("HOST", "localhost")
TASKS_REDIS_PORT = TASKS_REDIS.get("PORT", 6379)
TASKS_REDIS_SENTINELS = TASKS_REDIS.get("SENTINELS", [])
TASKS_REDIS_USING_SENTINEL = all(
    [isinstance(TASKS_REDIS_SENTINELS, list | tuple), len(TASKS_REDIS_SENTINELS) > 0]
)
TASKS_REDIS_SENTINEL_SERVICE = TASKS_REDIS.get("SENTINEL_SERVICE", "default")
TASKS_REDIS_SENTINEL_TIMEOUT = TASKS_REDIS.get("SENTINEL_TIMEOUT", 10)
TASKS_REDIS_USERNAME = TASKS_REDIS.get("USERNAME", "")
TASKS_REDIS_PASSWORD = TASKS_REDIS.get("PASSWORD", "")
TASKS_REDIS_DATABASE = TASKS_REDIS.get("DATABASE", 0)
TASKS_REDIS_SSL = TASKS_REDIS.get("SSL", False)
TASKS_REDIS_SKIP_TLS_VERIFY = TASKS_REDIS.get("INSECURE_SKIP_TLS_VERIFY", False)
TASKS_REDIS_CA_CERT_PATH = TASKS_REDIS.get("CA_CERT_PATH", False)
TASKS_REDIS_UNIX_SOCKET_PATH = TASKS_REDIS.get("UNIX_SOCKET_PATH", "")

# Caching
if "caching" not in REDIS:
    raise ImproperlyConfigured(
        "REDIS section in configuration.py is missing caching subsection."
    )
CACHING_REDIS = REDIS["caching"]
CACHING_REDIS_HOST = CACHING_REDIS.get("HOST", "localhost")
CACHING_REDIS_PORT = CACHING_REDIS.get("PORT", 6379)
CACHING_REDIS_DATABASE = CACHING_REDIS.get("DATABASE", 0)
CACHING_REDIS_USERNAME = CACHING_REDIS.get("USERNAME", "")
CACHING_REDIS_USERNAME_HOST = "@".join(
    filter(None, [CACHING_REDIS_USERNAME, CACHING_REDIS_HOST])
)
CACHING_REDIS_PASSWORD = CACHING_REDIS.get("PASSWORD", "")
CACHING_REDIS_SENTINELS = CACHING_REDIS.get("SENTINELS", [])
CACHING_REDIS_SENTINEL_SERVICE = CACHING_REDIS.get("SENTINEL_SERVICE", "default")
CACHING_REDIS_PROTO = "rediss" if CACHING_REDIS.get("SSL", False) else "redis"
CACHING_REDIS_SKIP_TLS_VERIFY = CACHING_REDIS.get("INSECURE_SKIP_TLS_VERIFY", False)
CACHING_REDIS_CA_CERT_PATH = CACHING_REDIS.get("CA_CERT_PATH", False)
CACHING_REDIS_UNIX_SOCKET_PATH = CACHING_REDIS.get("UNIX_SOCKET_PATH", "")


if CACHING_REDIS_UNIX_SOCKET_PATH:
    CACHING_REDIS_LOCATION = (
        f"unix://{CACHING_REDIS_UNIX_SOCKET_PATH}?db={CACHING_REDIS_DATABASE}"
    )
else:
    CACHING_REDIS_LOCATION = f"{CACHING_REDIS_PROTO}://{CACHING_REDIS_USERNAME_HOST}:{CACHING_REDIS_PORT}/{CACHING_REDIS_DATABASE}"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": CACHING_REDIS_LOCATION,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": CACHING_REDIS_PASSWORD,
        },
    }
}

if TASKS_REDIS_USING_SENTINEL:
    RQ_PARAMS = {
        "SENTINELS": TASKS_REDIS_SENTINELS,
        "MASTER_NAME": TASKS_REDIS_SENTINEL_SERVICE,
        "SOCKET_TIMEOUT": None,
        "CONNECTION_KWARGS": {"socket_connect_timeout": TASKS_REDIS_SENTINEL_TIMEOUT},
    }
else:
    RQ_PARAMS = {
        "HOST": TASKS_REDIS_HOST,
        "PORT": TASKS_REDIS_PORT,
        "SSL": TASKS_REDIS_SSL,
        "SSL_CERT_REQS": None if TASKS_REDIS_SKIP_TLS_VERIFY else "required",
    }

if TASKS_REDIS_UNIX_SOCKET_PATH:
    RQ_PARAMS = {
        "UNIX_SOCKET_PATH": TASKS_REDIS_UNIX_SOCKET_PATH,
        "DB": TASKS_REDIS_DATABASE,
    }
else:
    RQ_PARAMS.update(
        {
            "DB": TASKS_REDIS_DATABASE,
            "USERNAME": TASKS_REDIS_USERNAME,
            "PASSWORD": TASKS_REDIS_PASSWORD,
            "DEFAULT_TIMEOUT": RQ_DEFAULT_TIMEOUT,
        }
    )

if TASKS_REDIS_CA_CERT_PATH:
    RQ_PARAMS.setdefault("REDIS_CLIENT_KWARGS", {})
    RQ_PARAMS["REDIS_CLIENT_KWARGS"]["ssl_ca_certs"] = TASKS_REDIS_CA_CERT_PATH

RQ_QUEUES = {"high": RQ_PARAMS, "default": RQ_PARAMS, "low": RQ_PARAMS}
RQ_EXCEPTION_HANDLERS = ["core.exceptions.exception_handler"]

if LOGIN_TIMEOUT is not None:
    # Django default is 1209600 seconds (14 days)
    SESSION_COOKIE_AGE = LOGIN_TIMEOUT
SESSION_SAVE_EVERY_REQUEST = bool(LOGIN_PERSISTENCE)
if SESSION_FILE_PATH is not None:
    SESSION_ENGINE = "django.contrib.sessions.backends.file"


# Email
if EMAIL:
    EMAIL_HOST = EMAIL.get("SERVER")
    EMAIL_PORT = EMAIL.get("PORT", 25)
    EMAIL_HOST_USER = EMAIL.get("USERNAME")
    EMAIL_HOST_PASSWORD = EMAIL.get("PASSWORD")
    EMAIL_TIMEOUT = EMAIL.get("TIMEOUT", 10)
    SERVER_EMAIL = EMAIL.get("FROM_ADDRESS")
    EMAIL_SUBJECT_PREFIX = EMAIL.get("SUBJECT_PREFIX")
    EMAIL_USE_SSL = EMAIL.get("USE_SSL")
    EMAIL_USE_TLS = EMAIL.get("USE_TLS")
    EMAIL_SSL_KEYFILE = EMAIL.get("SSL_KEYFILE")
    EMAIL_SSL_CERTFILE = EMAIL.get("SSL_CERTFILE")
    EMAIL_CC_CONTACTS = EMAIL.get("CC_CONTACTS", [])
else:
    EMAIL_CC_CONTACTS = []

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "django_filters",
    "django_tables2",
    "rest_framework",
    "netfields",
    "social_django",
    "taggit",
    "bgp",
    "core",
    "devices",
    "extras",
    "messaging",
    "net",
    "peering",
    "peeringdb",
    "users",
    "utils",
    "webhooks",
    "django_rq",
    "drf_spectacular",
    "drf_spectacular_sidecar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "peering_manager.middleware.RemoteUserMiddleware",
    "peering_manager.middleware.CoreMiddleware",
]

# Django social auth
SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "peering_manager.authentication.user_default_groups_handler",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)

# Load all SOCIAL_AUTH_* settings from the user configuration
for param in dir(configuration):
    if param.startswith("SOCIAL_AUTH_"):
        globals()[param] = getattr(configuration, param)

# Force usage of PostgreSQL's JSONB field for extra data
SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_CLEAN_USERNAME_FUNCTION = (
    "peering_manager.authentication.utils.clean_username"
)

# Prometheus setup
if METRICS_ENABLED:
    PROMETHEUS_EXPORT_MIGRATIONS = False
    INSTALLED_APPS.append("django_prometheus")
    MIDDLEWARE = [
        "django_prometheus.middleware.PrometheusBeforeMiddleware",
        *MIDDLEWARE,
        "django_prometheus.middleware.PrometheusAfterMiddleware",
    ]
    configuration.DATABASE.update(
        {"ENGINE": "django_prometheus.db.backends.postgresql"}
    )

ROOT_URLCONF = "peering_manager.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "peering_manager.context_processors.settings",
                "peering_manager.context_processors.affiliated_autonomous_systems",
            ]
        },
    }
]

WSGI_APPLICATION = "peering_manager.wsgi.application"
SECURE_PROXY_SSL_HEADER = getattr(
    configuration, "SECURE_PROXY_SSL_HEADER", ("HTTP_X_FORWARDED_PROTO", "https")
)
USE_X_FORWARDED_HOST = getattr(configuration, "USE_X_FORWARDED_HOST", True)
X_FRAME_OPTIONS = "SAMEORIGIN"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
LANGUAGE_CODE = "en-us"
USE_I18N = True
USE_L10N = True


LOGIN_URL = f"/{BASE_PATH}login/"
# URLs exempt from login enforcement
AUTH_EXEMPT_PATHS = (
    LOGIN_URL,
    f"/{BASE_PATH}api/",
    f"/{BASE_PATH}oauth/",
    f"/{BASE_PATH}metrics",
)


# Messages
MESSAGE_TAGS = {messages.ERROR: "danger"}


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = f"/{BASE_PATH}static/"
STATICFILES_DIRS = (BASE_DIR / "project-static",)

# Django debug toolbar
INTERNAL_IPS = ["127.0.0.1", "::1"]

# Census collection
DEPLOYMENT_ID = hashlib.sha256(SECRET_KEY.encode("utf-8")).hexdigest()[:16]
CENSUS_URL = "https://census.peering-manager.net/api/v1/records/"
CENSUS_PARAMETERS = {
    "deployment_id": DEPLOYMENT_ID,
    "version": VERSION,
    "python_version": platform.python_version(),
}
if CENSUS_REPORTING_ENABLED and not DEBUG and "test" not in sys.argv:
    with contextlib.suppress(requests.RequestException):
        requests.post(
            CENSUS_URL, json=CENSUS_PARAMETERS, timeout=3, proxies=HTTP_PROXIES
        )
