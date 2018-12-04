import os
import logging
import pathlib

# This is a minimal configuration to get you started with the Text mode.
# If you want to connect Errbot to chat services, checkout
# the options in the more complete config-template.py from here:
# https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py

BACKEND = (
    "Slack"
)  # Errbot will start in text mode (console only mode) and will answer commands from there.

ROOT_DIR = pathlib.Path(__file__).parent
BOT_DATA_DIR = ROOT_DIR / "data"  # get config.py's dir
BOT_EXTRA_PLUGIN_DIR = ROOT_DIR / "plugins"

BOT_LOG_FILE = ROOT_DIR / "error.log"
BOT_LOG_LEVEL = logging.INFO

BOT_IDENTITY = {"token": os.getenv("SLACK_TOKEN")}

BOT_ADMINS = ("@aron",)
BOT_ALT_PREFIXES = ("@aronbot",)
