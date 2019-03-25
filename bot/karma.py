from . import IS_USER, MAX_POINTS, SLACK_CLIENT, karmas
from .slack import lookup_username, post_msg
import logging
import json
from bson import BSON, json_util

KARMABOT = 'karmabot'


def _parse_karma_change(karma_change):
    userid, voting = karma_change

    if IS_USER.match(userid):
        receiver = lookup_username(userid)
    else:
        receiver = userid.strip(' #').lower()

    points = voting.count('+') - voting.count('-')

    return receiver, points


def process_karma_changes(message, karma_changes):
    for karma_change in karma_changes:
        giver = lookup_username(message.giverid)
        channel = message.channel

        receiver, points = _parse_karma_change(karma_change)

        karma = Karma(giver, receiver)

        try:
            msg = karma.change_karma(points)
        except Exception as exc:
            msg = str(exc)

        post_msg(channel, msg)


class Karma:

    def __init__(self, giver, receiver):
        self.giver = giver
        self.receiver = receiver
        self.last_score_maxed_out = False

    def _calc_final_score(self, points):
        if abs(points) > MAX_POINTS:
            self.last_score_maxed_out = True
            return MAX_POINTS if points > 0 else -MAX_POINTS
        else:
            self.last_score_maxed_out = False
            return points

    def _create_msg_bot_self_karma(self, points):
        rec = karmas.find_one({"user":self.receiver})
        logging.debug(rec)
        receiver_karma = rec['karma']
        logging.debug(receiver_karma)
        if points > 0:
            msg = 'Thanks @{} for the extra karma'.format(self.giver)
            msg += ', my karma is {} now'.format(receiver_karma)
        else:
            msg = 'Not cool @{} lowering my karma to {}'.format(self.giver,
                                                                receiver_karma)
            msg += ', but you are probably right'
            msg += ', I will work harder next time'
        return msg

    def _create_msg(self, points):

        userinfo = SLACK_CLIENT.api_call("users.info", user=self.receiver)
        username = userinfo['user']['name']

        poses = "'" if username.endswith('s') else "'s"
        action = 'increase' if points > 0 else 'decrease'
        rec = karmas.find_one({"user":self.receiver})
        receiver_karma = rec['karma']

        msg = '{}{} karma {}d to {}'.format(username,
                                            poses,
                                            action,
                                            receiver_karma)
        if self.last_score_maxed_out:
            msg += ' (= max {} of {})'.format(action, MAX_POINTS)

        return msg

    def change_karma(self, points):
        '''updates karmas dict and returns message string'''
        userinfo = SLACK_CLIENT.api_call("users.info", user=self.receiver)
        if userinfo['ok']:
            if not isinstance(points, int):
                err = ('Program bug: change_karma should '
                       'not be called with a non int for '
                       'points arg!')
                raise RuntimeError(err)

            if self.giver == self.receiver:
                raise ValueError('Sorry, cannot give karma to self')
                #raise ValueError(self.giver)

            points = self._calc_final_score(points)
            karmas.update_one({"user":self.receiver},{"$inc":{"karma":1}})

            if self.receiver == KARMABOT:
                return self._create_msg_bot_self_karma(points)
            else:
                return self._create_msg(points)
