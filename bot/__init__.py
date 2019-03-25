from collections import Counter
import logging
import os
import pickle
import re
import sys
from pymongo import MongoClient
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

client = MongoClient('mongodb://localhost:27017')
db = client.local
karmas = db.karma

if not client:
    print('Mongo Database not started')
    sys.exit(1)

#check if database exists?


KARMA_BOT = botuser
SLACK_CLIENT = SlackClient(token)

MAX_POINTS = 2

# the first +/- is merely signaling, start counting (regex capture)
# from second +/- onwards, so bob++ adds 1 point, bob+++ = +2, etc
KARMA_ACTION = re.compile(r'(?:^| )(\S{2,}?)\s?[\+\-]([\+\-]+)')
IS_USER = re.compile(r'^<@[^>]+>$')

#USERNAME_CACHE = {}
#KARMA_CACHE = 'data'

logging.info('Script started')

#try:

    #logging.info('Retrieving karma cache file')
    #karmas = pickle.load(open(KARMA_CACHE, "rb"))
#except FileNotFoundError:
    #logging.info('No cache file starting new Counter object in memory')
    #karmas = Counter()
