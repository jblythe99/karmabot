import logging
import sys
import time

from bot import SLACK_CLIENT, KARMA_ACTION
from bot.slack import parse_next_msg
from bot.karma import process_karma_changes

SAVE_INTERVAL = 60

# Slack Real Time Messaging API - https://api.slack.com/rtm
if not SLACK_CLIENT.rtm_connect():
    logging.error('Connection Failed, invalid token?')
    sys.exit(1)

def main():
    try:
        count = 0
        while True:
            count += 1

            message = parse_next_msg()
            if not message:
                continue

            karma_changes = KARMA_ACTION.findall(message.text)
            if not karma_changes:
                continue

            logging.debug('karma changes: {}'.format(str(karma_changes)))
            """add exclusion list for channels to do karma in"""
            """give feedback if channel does not accept karma?"""
            process_karma_changes(message, karma_changes)
    finally:
        logging.info('Script ended, saving karma cache to file')
        # making sure we store karma cache before exiting the script, see
        # https://stackoverflow.com/questions/3850261/doing-something-before-program-exit
        #_save_cache()


if __name__ == '__main__':
    main()
