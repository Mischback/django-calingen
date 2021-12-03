# SPDX-License-Identifier: MIT

# local imports
from .settings_test import *

INSTALLED_APPS += [
    "debug_toolbar",
]

# Enable Django's DEBUG mode
DEBUG = True

MIDDLEWARE += [
    # add DebugToolbar middleware
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

CALINGEN_EXTERNAL_EVENT_PROVIDER = [
    "calingen.contrib.holidays.germany",
]

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
