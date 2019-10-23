import logging

# This is a minimal configuration to get you started with the Text mode.
# If you want to connect Errbot to chat services, checkout
# the options in the more complete config-template.py from here:
# https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py

BACKEND = (
    "Slack"
)  # Errbot will start in text mode (console only mode) and will answer commands from there.
BOT_IDENTITY = {"token": "xoxb-266216378434-783351198945-vj2OvFmVFeibdGueXMWQ9k8y"}

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


BOT_DATA_DIR = r"/Users/craig/Source Code/vectra.ai/Python/cogbot/cogbot/src/data"
BOT_EXTRA_PLUGIN_DIR = (
    r"/Users/craig/Source Code/vectra.ai/Python/cogbot/cogbot/src/plugins"
)

BOT_LOG_FILE = r"/Users/craig/Source Code/vectra.ai/Python/cogbot/cogbot/src/errbot.log"
BOT_LOG_LEVEL = logging.DEBUG

