# -*- coding: utf-8 -*-

from juggernaut import Juggernaut, RedisRoster


def get_roster(group_id):
    """ Return roster of the given group. """
    jug = Juggernaut()
    jug.meta = {'group_id': group_id}
    return RedisRoster(jug, user_meta_key='group_id')


# from juggernaut import Juggernaut, RedisRoster
# jug = Juggernaut()
# jug.meta = {'group_id': 1}
# roster = RedisRoster(jug, user_meta_key='group_id')