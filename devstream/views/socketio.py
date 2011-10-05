# -*- coding: utf-8 -*-

import redis
import logging
from json import loads

from pyramid.view import view_config
from pyramid.response import Response

from pyramid_socketio.io import SocketIOContext, socketio_manage

log = logging.getLogger(__name__)


class ConnectIOContext(SocketIOContext):
    def msg_connect(self, msg):
        log.debug("User %s connected" % msg['uid'])

        def redis_listener():
            """ Redis listener for publishing messages. """
            rdis = redis.Redis()

            # create/retrieve a pubsub object
            pubsub = rdis.pubsub()

            # subscribe to channel
            pubsub.subscribe(['devstream'])
            log.debug("User %s has been subscribed" % msg['uid'])

            # send all messages
            for message in pubsub.listen():
                if not self.io.connected():
                    return
                log.debug("Redis: %s" % message)
                if message['type'] == 'message':
                    self.io.send(loads(message['data']))

        # spawn redis listener for each connected user
        self.spawn(redis_listener)


@view_config(route_name="socket_io")
def socketio_service(request):
    print "Socket.IO request running"
    retval = socketio_manage(ConnectIOContext(request))
    return Response(retval)
