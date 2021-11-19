# SPDX-License-Identifier: MIT

# local imports
from .settings_test import *

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "tests.util.callback_show_debug_toolbar",
}
