import logging
import os

# This is a minimal configuration to get you started with the Text mode.
# If you want to connect Errbot to chat services, checkout
# the options in the more complete config-template.py from here:
# https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py
slack_token = os.getenv("SLACK_TOKEN")

BACKEND = (
    "Slack"
)  # Errbot will start in text mode (console only mode) and will answer commands from there.
BOT_IDENTITY = {"token": slack_token}

BOT_ADMINS = ("@craig",)
BOT_ALT_PREFIXES = "@cogbot"
CORE_PLUGINS = (
    "ACLs",
    "Flows",
    "CommandNotFoundFilter",
    "Health",
    "Help",
    "TextCmds",
    "Plugins",
    "Logger",
)


BOT_DATA_DIR = r"./data"
BOT_EXTRA_PLUGIN_DIR = r"./plugins"

BOT_LOG_FILE = r"./errbot.log"
BOT_LOG_LEVEL = logging.DEBUG

