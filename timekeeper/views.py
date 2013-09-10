import datetime
import pytz

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
    BillingPeriod,
    )

from .security import authenticate_user

from . import fuzzy_date, util

@view_config(route_name='dashboard', renderer='timekeeper:templates/dashboard.mak',
             permission='clock')
def dashboard(request):
    user_id = authenticated_userid(request)

    user = DBSession.query(Employee).get(user_id)
    projects = DBSession.query(Project).all()

    current_session = user.get_current_session()

    return dict(
            message='',
            user=user,
            projects=projects,
            current_session=user.get_current_session()
            )

@view_config(route_name='clock_in', request_method='POST', permission='clock')
def clock_in(request):
    user_id = authenticated_userid(request)
    user = DBSession.query(Employee).get(user_id)

    time_override = request.params.get('time_override', None)
    if time_override:
        localtz = pytz.timezone(request.registry.settings['local_timezone'])
        current_datetime = util.utcnow().astimezone(localtz)

        local_timestamp = fuzzy_date.parse_fuzzy_datetime(
                request.params['time_override'], current_datetime)
        if not local_timestamp:
            raise ValueError('Invalid date format')
        timestamp = localtz.localize(local_timestamp).astimezone(pytz.utc)
    else:
        timestamp = util.utcnow()

    user.close_current_session(timestamp)

    if 'projectname' in request.params:
        project_name = request.params['projectname']
        project = Project.get_by_name(project_name)

        session = WorkSession(
                employee=user,
                project=Project.get_by_name(project_name),
                start_time=timestamp,
                billing_period=BillingPeriod.get_current())
        DBSession.add(session)

    return HTTPFound(location=request.route_url('dashboard'))

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
