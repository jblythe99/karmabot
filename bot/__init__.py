from collections import Counter
import logging
import os
import re
import sys

import pkgutil
import importlib
from typing import List

import bot
from bot.base import REGISTERED_CLASSES

pkg = bot

from slackclient import SlackClient

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',  # noqa E501
                    datefmt='%m-%d %H:%M',
                    filename='bot.log')

botuser = os.environ.get('SLACK_KARMA_BOTUSER')
token = os.environ.get('SLACK_KARMA_TOKEN')
if not botuser or not token:
    print('Make sure you set SLACK_KARMA_BOTUSER and SLACK_KARMA_TOKEN in env')
    sys.exit(1)

for mod_info in pkgutil.iter_modules(pkg.__path__):
    if mod_info.name.startswith('connectors'):
        module = importlib.import_module('bot.'+mod_info.name)
        module_path: List[str] = module.__path__
        for pkg_info in pkgutil.walk_packages(module_path, module.__name__+'.'):
            importlib.import_module(pkg_info.name)


store = REGISTERED_CLASSES['MONGO']()
conn = store.get_connection()
karmas = store.get_karmas(conn)

#check if database exists?


KARMA_BOT = botuser
SLACK_CLIENT = SlackClient(token)

MAX_POINTS = 2

# the first +/- is merely signaling, start counting (regex capture)
# from second +/- onwards, so bob++ adds 1 point, bob+++ = +2, etc
KARMA_ACTION = re.compile(r'(?:^| )(\S{2,}?)\s?[\+\-]([\+\-]+)')
IS_USER = re.compile(r'^<@[^>]+>$')



logging.info('Script started')