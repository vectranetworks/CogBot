# CogBot
CogBot is a chatbot for Cognito Detect

## Getting started

Requirements:
- Python 3.6+
- Python Virtualenv (virtualenv, pyenv-virtualenv, pipenv and others should all work.)
- ErrBot (Python library)
- Reqests (Python Library)


To deploy CogBot here are some general steps and guidelines.  This is NOT the only way to install and configure CogBot.

1.  Create a virtualenv using python 3.6+ if using pyenv and pyenv-virtualenv then.
    1.  pyenv install 3.7.3
    2.  pyenv virtualenv 3.7.3 cogbot
    3.  source /path/to/cogbog/venv/bin/activate
2.  Using git, clone the CobBot git repo to a local directory
3.  Enter the CogBot directory
4.  Initalize CogBot
    1.  errbot --init
5.  Modily the config.py file to connect to your chosen chat backend.
