# -*- coding: utf-8 -*-
from wsgiref import util
from watson.cors import decorators
from watson.di import container
from watson.events import types
from watson.http import messages
from watson.routing import routes


def sample_environ(**kwargs):
    environ = {}
    util.setup_testing_defaults(environ)
    environ.update(kwargs)
    return environ


class SampleController(object):
    @decorators.cors
    def GET(self):
        pass


class TestDecorator(object):
    def test_response(self):
        ioc = container.IocContainer()
        ioc.add('application.config', {
            'cors': {},
        })
        route = routes.Literal(
            name='test', path='/', accepts=('GET', 'OPTIONS'))
        route_match = routes.RouteMatch(route=route, params={})
        response = messages.Response()
        request = messages.Request.from_environ(
            sample_environ(REQUEST_METHOD='OPTIONS'))
        event = types.Event(
            name='test',
            params={
                'context': {
                    'response': response,
                    'request': request,
                    'route_match': route_match
                }
            })
        controller = SampleController()
        controller.event = event
        controller.container = ioc
        controller.request = request
        controller.response = response
        controller.GET()
        assert response._cors_processed
