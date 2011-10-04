# -*- coding: utf-8 -*-

import os
import pkg_resources
from datetime import timedelta, datetime


def assets_url(request, path):
    """ Return a versioned URL for an asset.

    The versioning scheme consists in basing the version number upon the file's
    last modified time and appending it to the given path as a query string.

    """
    asset_path = pkg_resources.resource_filename('devstream', 'static' + path)
    modified = int(os.stat(asset_path).st_mtime)
    return "%s?v=%d" % (request.static_url('devstream:static' + path), modified)


def get_settings(request, key, default=''):
    setting = request.registry.settings.get(key, default)
    if setting and key == 'meta_expires':
        duration_unit = {'h': 'hours', 'd': 'days', 'w': 'weeks'}
        duration = duration_unit.get(setting[-1], None)
        if not duration:
            raise Exception("Unknown meta_expires settings '%s'" % setting)
        d = datetime.now() + timedelta(**{duration: int(setting[:-1])})
        setting = d.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return setting
