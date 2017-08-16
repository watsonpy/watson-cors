# -*- coding: utf-8 -*-
from wsgiref import util
from watson.cors import listeners
from watson.di import container
from watson.events import types
from watson.http import messages
from watson.routing import routes


def sample_environ(**kwargs):
    environ = {}
    util.setup_testing_defaults(environ)
    environ.update(kwargs)
    return environ


class TestRequest(object):
    def test_response(self):
        ioc = container.IocContainer()
        ioc.add('application.config', {
            'cors': {},
        })
        route = routes.Literal(
            name='test', path='/', accepts=('GET', 'OPTIONS'))
        route_match = routes.RouteMatch(route=route, params={})
        response = messages.Response()
        event = types.Event(
            name='test',
            params={
                'context': {
                    'response': response,
                    'request': messages.Request.from_environ(
                        sample_environ(REQUEST_METHOD='OPTIONS')),
                    'route_match': route_match
                }
            })
        listener = listeners.Request()
        listener.container = ioc
        listener(event)
        assert response._cors_processed
