"""
Constants used in this app
"""

# Standard Library
import os

# Alliance Auth
from esi import __version__ as esi_version

# AA Fleet Finder
from fleetfinder import __version__

AA_FLEETFINDER_BASE_DIR = os.path.join(os.path.dirname(__file__))
AA_FLEETFINDER_STATIC_DIR = os.path.join(
    AA_FLEETFINDER_BASE_DIR, "static", "fleetfinder"
)

APP_NAME = "aa-fleetfinder"
GITHUB_URL = f"https://github.com/ppfeufer/{APP_NAME}"
USER_AGENT = f"{APP_NAME}/{__version__} ({GITHUB_URL}) via django-esi/{esi_version}"
