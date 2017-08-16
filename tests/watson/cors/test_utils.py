# -*- coding: utf-8 -*-
from wsgiref import util
from watson.cors import utils
from watson.http import messages
from watson.di import container
from watson.routing import routes


def sample_environ(**kwargs):
    environ = {}
    util.setup_testing_defaults(environ)
    environ.update(kwargs)
    return environ


def sample_cors_options(**kwargs):
    options = {
        'allow_origin': '*',
        'allow_credentials': False,
        'allow_methods': None,
        'allow_headers': None,
        'expose_headers': None,
        'max_age': -1
    }
    options.update(kwargs)
    return options


class TestUtils(object):
    def test_generate_cors_config(self):
        ioc = container.IocContainer()
        ioc.add('application.config', {
            'cors': {},
        })
        route = routes.Literal(
            name='test', path='/', accepts=('GET', 'OPTIONS'))
        config = utils.generate_cors_config(ioc, route)
        assert config['allow_methods'] == ('GET', 'OPTIONS')

    def test_preflight_check(self):
        request = messages.Request.from_environ(sample_environ(REQUEST_METHOD='OPTIONS'))
        response = messages.Response()
        options = sample_cors_options(
            allow_headers=('authorization',),
            allow_methods=('GET', 'OPTIONS'))
        utils.process_cors(
            request,
            response,
            **options)
        assert response._cors_processed
        assert 'authorization' in response.headers.get('Access-Control-Allow-Headers')
        assert utils.process_cors(request, response, **options)

    def test_allow_origin(self):
        request = messages.Request.from_environ(sample_environ())
        response = messages.Response()
        utils.process_cors(
            request,
            response,
            **sample_cors_options())
        assert response._cors_processed
        assert response.headers.get('Access-Control-Allow-Origin') == '*'

    def test_allow_origin_list(self):
        request = messages.Request.from_environ(sample_environ(HTTP_ORIGIN='http://127.0.0.1'))
        response = messages.Response()
        utils.process_cors(
            request,
            response,
            **sample_cors_options(allow_origin=('http://127.0.0.1', 'google.com')))
        assert response._cors_processed
        assert 'http://127.0.0.1' == response.headers.get('Access-Control-Allow-Origin')

    def test_allow_credentials(self):
        request = messages.Request.from_environ(sample_environ())
        response = messages.Response()
        utils.process_cors(
            request,
            response,
            **sample_cors_options(allow_credentials=True))
        assert response._cors_processed
        assert response.headers.get('Access-Control-Allow-Credentials') == 'true'

    def test_expose_headers(self):
        request = messages.Request.from_environ(sample_environ())
        response = messages.Response()
        utils.process_cors(
            request,
            response,
            **sample_cors_options(expose_headers=('authorization',)))
        assert response._cors_processed
        assert 'authorization' in response.headers.get('Access-Control-Expose-Headers')
