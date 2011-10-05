# -*- coding: utf-8 -*-

from pyramid.view import view_config
from pyramid.response import Response

from pyramid_socketio.io import SocketIOContext, socketio_manage


class ConnectIOContext(SocketIOContext):
    def msg_connect(self, msg):
        pass


@view_config(route_name="socket_io")
def socketio_service(request):
    print "Socket.IO request running"
    retval = socketio_manage(ConnectIOContext(request))
    return Response(retval)
