# F1-Bot
Code of F1-Bot

## Basic structure

The bot should be run via `main.py`. In order to run this, you will also need a botData.py file which contains all passwords and keys for the APIs. This file is naturally not included.

The `main.py` file in turn calls `injected.py` in a loop, which allows us to update the bot while it is running. All functionality of the bot is devided between the other Python files, for a more logical structure and improved readability.
