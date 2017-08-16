Usage
=====

There are several ways you can implement CORS support into your Watson project.

1. Managed via @decorators in your controllers
2. Managed via route definitions
3. Managed via event listeners

Default Configuration
---------------------

These configuration options are passed by default into your decorators or
listeners.

.. code-block:: python

    defaults = {
        'allow_origin': None,
        'allow_credentials': False,
        'allow_methods': (
            'DELETE',
            'GET',
            'OPTIONS',
            'PATCH',
            'POST',
            'PUT',
        ),
        'allow_headers': (
            'accept',
            'accept-encoding',
            'authorization',
            'content-type',
            'dnt',
            'origin',
            'user-agent',
            'x-csrftoken',
            'x-requested-with',
        ),
        'expose_headers': None,
        'max_age': 86400,
    }

For acceptable values for each of these, please read https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS

Option Types
------------

allow_origin
    list|string: The allowed origin(s) for the request
allow_credentials
    boolean: Whether or not credentials are allowed
allow_methods
    list: The HTTP request methods that are allowed
allow_headers
    list: The HTTP headers that are allowed
expose_headers
    list: The HTTP headers which should be exposed
max_age
    integer: The length of time in seconds the OPTIONS response can be cached


Configuration Fallbacks
-----------------------

Whenever the listener or decorator is invoked, the following order of
inheritance of options will be used when processing the request:

1. The default configuration (`watson.cors.config.defaults`)
2. The application configuration
3. The route configuration (specify the arguments in the `options`
    property)
4. The decorator arguments


Dynamic Allowed Origins
-----------------------

The preferred way to approach this issue would be to subclass `watson.cors.listeners.Request`
and then modify the arguments that are sent through to `watson.cors.utils.process_cors`.

Configuring CORS
================

In addition to the individual ways to configure CORS, you can also take
advantage of the way the configuration is inherited, and define common values
in your application configuration.

.. code-block:: python

    # config.py

    cors = {
        'allow_origin': 'http://127.0.0.1',
        'allow_credentials': True
    }


Via Decorators
--------------

.. code-block:: python

    # controllers.py

    from watson.cors.decorators import cors
    from watson.framework import controllers
    from watson.framework.views.decorators import view

    class MyController(controllers.Rest):

        @view(format='json')
        @cors(allow_origin='http://127.0.0.1', allow_credentials=True)
        def GET(self):
            pass

        @cors(allow_origin='http://127.0.0.1', allow_credentials=True)
        def OPTIONS(self):
            return self.response


If you have already set the options in your application configuration, you can
simply decorate the method with `@cors`.


Via Event Listener
------------------

.. code-block:: python

    # config.py

    cors = {
        'allow_origin': 'http://127.0.0.1',
        'allow_credentials': True
    }

    events = {
        events.DISPATCH_EXECUTE: [
            ('watson.cors.listeners.Request',)
        ]
    }


Via Routes
----------

Routes modify the `allow_methods` option in a slightly different way to
the other ways of configuring CORS. Any items set in the `accepts` property
will override `allow_methods`.

.. code-block:: python

    # config.py

    routes {
        'allow_origin': 'http://127.0.0.1',
        'allow_credentials': True
    }

    events = {
        events.DISPATCH_EXECUTE: [
            ('watson.cors.listeners.Request',)
        ]
    }

    routes = {
        'cors-request': {
            'path': '/cors',
            'options': {
                'controller': 'app.controllers.CorsRequest',
                'cors': {
                    'expose_headers': ('my-custom-header',)
                }
            },
            'accepts': ('GET', 'OPTIONS')
        },
    }
