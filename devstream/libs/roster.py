# -*- coding: utf-8 -*-

import os
import logging
from juggernaut import Juggernaut, RedisRoster

from flaskext.sqlalchemy import SQLAlchemy

from devstream.models import User


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__file__)

class ChannelRoster(RedisRoster):
    """ Extends the RedisRoster by
    clustering online users using channels. """

    def __init__(self, db=None, jug=None, key_prefix='juggernaut-roster:',
                 user_meta_key='user_id'):
        super(ChannelRoster, self).__init__(jug, key_prefix, user_meta_key)
        self.db = db

    def on_signed_in(self, user_id, channel):
        """Called if a user is signed in."""
        log.debug("Login: %s" % user_id)
        log.debug(channel)
        user = self.db.session.query(User).get(int(user_id))
        self.jug.publish(channel, {'msg_type': 'login',
                                   'user_id': user_id,
                                   'email': user.email,
                                   'username': user.username})
    
    def on_signed_out(self, user_id, channel):
        """Called if a user signs out."""
        log.debug("Logout: %s" % user_id)
        log.debug(channel)
        user = self.db.session.query(User).get(int(user_id))
        self.jug.publish(channel, {'msg_type': 'logout',
                                   'user_id': user_id,
                                   'email': user.email,
                                   'username': user.username})

    def get_online_users(self, channel):
        """ Retrieve online users from redis and returns user objects. """
        key = '%schannel-active:%s' % (self.key_prefix, channel)
        return self.jug.redis.smembers(key)

    def on_subscribe(self, user_id, data):
        r = self.jug.redis
        key = '%sconnections:%s' % (self.key_prefix, user_id)
    
        # if adding wen't success, then the user has just signed in.
        # call on_signed_in hook.
        if r.sadd(key, data['session_id']):
            # add user to channel's active members
            key = '%schannel-active:%s' % (self.key_prefix, data['channel'])
            r.sadd(key, user_id)

            # call login callback
            self.on_signed_in(user_id, data['channel'])
        r.sadd(self.key_prefix + 'online-users', user_id)

    def on_unsubscribe(self, user_id, data):
        r = self.jug.redis
        key = '%sconnections:%s' % (self.key_prefix, user_id)
    
        # if removing was successful, call on_signed_out hook.
        if r.srem(key, data['session_id']):
            # remove user from channel's active members
            key = '%schannel-active:%s' % (self.key_prefix, data['channel'])
            r.srem(key, user_id)

            # call logout callback
            self.on_signed_out(user_id, data['channel'])


def _run_roster(app):
    db = SQLAlchemy(app=app)
    roster = ChannelRoster(db=db, jug=Juggernaut())
    roster.run()


def get_online_users(group_id):
    """ Helper function that actually returns online
    user objects instead of just uids. """
    roster = ChannelRoster(jug=Juggernaut())
    online_users = roster.get_online_users('group%s' % group_id)
    for user_id in online_users:
        user = User.query.get(int(user_id))
        online_users.remove(user_id)
        online_users.add(user)
    return online_users
