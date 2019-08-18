import logging

# This is a minimal configuration to get you started with the Text mode.
# If you want to connect Errbot to chat services, checkout
# the options in the more complete config-template.py from here:
# https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py

BACKEND = (
    "Slack"
)  # Errbot will start in text mode (console only mode) and will answer commands from there.

BOT_DATA_DIR = r"/Users/craigsimon/Source Code/vectra.ai/Python/cogbot/cogbot/src/data"
BOT_EXTRA_PLUGIN_DIR = (
    r"/Users/craigsimon/Source Code/vectra.ai/Python/cogbot/cogbot/src/plugins"
)

BOT_LOG_FILE = (
    r"/Users/craigsimon/Source Code/vectra.ai/Python/cogbot/cogbot/src/errbot.log"
)
BOT_LOG_LEVEL = logging.DEBUG

BOT_ADMINS = (
    "@craig",
    "twade",
    "jbarrett",
)  # !! Don't leave that to "@CHANGE_ME" if you connect your errbot to a chat system !!

BOT_IDENTITY = {"token": "xoxb-718682728370-730129281024-Uz67OCbayLhPnmf11bOqy9Ke"}

