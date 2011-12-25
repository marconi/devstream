# -*- coding: utf-8 -*-

from .status import Status
from .group import Group


def as_status(item_dict):
    """ Return a status object based on item_dict. """
    return Status(status=item_dict['status'],
                  type=item_dict['type'].upper(),
                  group_id=int(item_dict['group_id']))


def as_group(item_dict):
    """ Return a group object based on item_dict. """
    return Group(name=item_dict['name'])
