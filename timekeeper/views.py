from pyramid.response import Response
from pyramid.view import (
        view_config,
        forbidden_view_config,
        )
from pyramid.security import (
        remember,
        forget,
        authenticated_userid,
        )
from pyramid.httpexceptions import (
        HTTPFound,
        )
from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Employee,
    Project,
    WorkSession,
    )

from .security import authenticate_user

@view_config(route_name='dashboard', renderer='timekeeper:templates/dashboard.mak',
             permission='clock')
def dashboard(request):
    user_id = authenticated_userid(request)
    user = DBSession.query(Employee).get(user_id)
    projects = DBSession.query(Project).all()

    current_session = DBSession.query(WorkSession).filter_by(employee_id=user.id, end_time=None).first()

    if current_session is not None:
        current_project_name = current_session.project.name
    else:
        current_project_name = "None"

    return dict(
            request=request, # For route_url
            message='',
            user=user,
            projects=projects,
            current_project_name=current_project_name,
            )

@view_config(route_name='clock_in', renderer='timekeeper:templates/dashboard.mak',
             permission='clock')
def clock_in(request):
    pass

@view_config(route_name='admin', renderer='timekeeper:templates/dashboard.mak',
             permission='manage')
def admin(request):
    pass

@view_config(route_name='login', renderer='timekeeper:templates/login.mak')
@forbidden_view_config(renderer='timekeeper:templates/login.mak')
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
