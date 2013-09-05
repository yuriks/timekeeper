from pyramid.response import Response
from pyramid.view import (
        view_config,
        forbidden_view_config,
        )
from pyramid.security import (
        remember,
        forget,
        )
from pyramid.httpexceptions import (
        HTTPFound,
        )
from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    )

from .security import authenticate_user

@view_config(route_name='login', renderer='templates/login.pt')
@forbidden_view_config(renderer='templates/login.pt')
def login(request):
    message = ''
    login = ''

    if request.method == 'POST':
        login = request.params['login']
        password = request.params['password']

        user = authenticate_user(login, password)
        if user:
            headers = remember(request, user.id)
            return HTTPFound(location = request.application_url,
                             headers = headers)
        message = "Login failed."

    return dict(
            message = message,
            url = request.route_url('login'),
            login = login,
            )

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.application_url,
                     headers = headers)
