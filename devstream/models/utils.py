# -*- coding: utf-8 -*-

from .status import Status


def as_status(item_dict):
    """ Return a status object based on item_dict. """
    return Status(status=item_dict['status'],
                  type=item_dict['type'].upper())
