# -*- coding: utf-8 -*-

def add_routes(config):
    config.add_route('socket_io', 'socket.io/*remaining')
    config.add_route('home', '/')

    # status
    config.add_route('post_status', '/status/post')
