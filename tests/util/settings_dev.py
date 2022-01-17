# SPDX-License-Identifier: MIT

# Django imports
from django.utils.translation import gettext_noop as _

# local imports
from .settings_test import *

INSTALLED_APPS += [
    "calingen.contrib.layouts.simple_event_list",
    "calingen.contrib.layouts.year_by_week",
    "calingen.contrib.layouts.lineatur",
    "debug_toolbar",
]

# Enable Django's DEBUG mode
DEBUG = True

# Re-enable Internationalization (turned off iin settings_test.py)
USE_I18N = True

# enable Localization
USE_L10N = True

# enable timezone awareness by default
USE_TZ = True

LANGUAGES = (("en", _("English")), ("de", _("German")))

MIDDLEWARE += [
    # add DebugToolbar middleware
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# Inject the localization middleware into the right position
MIDDLEWARE = [
    y
    for i, x in enumerate(MIDDLEWARE)
    for y in (
        ("django.middleware.locale.LocaleMiddleware", x)
        if MIDDLEWARE[i - 1] == "django.contrib.sessions.middleware.SessionMiddleware"
        else (x,)
    )
]

CALINGEN_EXTERNAL_EVENT_PROVIDER = [
    "calingen.contrib.providers.germany",
]

CALINGEN_COMPILER = {
    "default": "calingen.contrib.compilers.copy_paste.compiler.CopyPasteCompiler",
    "html": "calingen.contrib.compilers.html_or_download.compiler.HtmlOrDownloadCompiler",
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "dev_f": {
            "format": "[%(levelname)s] %(name)s:%(lineno)d:%(funcName)s \n\t %(message)s",
        },
    },
    "handlers": {
        "def_h": {
            "class": "logging.StreamHandler",
            "formatter": "dev_f",
        },
    },
    "loggers": {
        "calingen": {
            "handlers": ["def_h"],
            "level": "DEBUG",
            "propagate": False,
        }
    },
}


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "tests.util.callback_show_debug_toolbar",
}
