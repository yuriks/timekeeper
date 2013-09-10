from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.events import BeforeRender
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )

from .security import authentication_policy
from . import template_helpers

def add_renderer_globals(event):
    event['h'] = template_helpers

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    authn_policy = AuthTktAuthenticationPolicy(
            'p6Qt9Yd0qW8e4CwvoLaf', callback=authentication_policy,
            hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings,
                          root_factory='timekeeper.security.RootFactory')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_subscriber(add_renderer_globals, BeforeRender)

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('dashboard', '/')
    config.add_route('clock_in', '/clock_in')
    config.add_route('admin', '/admin')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.scan()
    return config.make_wsgi_app()
