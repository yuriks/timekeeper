import pytz

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    Boolean,
    DateTime,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    object_session,
    )

from sqlalchemy.types import TypeDecorator

from zope.sqlalchemy import ZopeTransactionExtension

from . import util

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class UTCDateTime(TypeDecorator):
    impl = DateTime

    def process_bind_param(self, value, engine):
        if value is not None:
            return value.astimezone(pytz.utc)

    def process_result_value(self, value, engine):
        if value is not None:
            return pytz.utc.localize(value)


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @classmethod
    def get_by_name(cls, project_name):
        return DBSession.query(cls).filter_by(name=project_name).one()

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    login = Column(Text, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    active = Column(Boolean, nullable=False)
    admin = Column(Boolean, nullable=False)
    hourly_rate = Column(Numeric(precision=6, scale=2), nullable=False)

    def __init__(self, login, password_hash, name, hourly_rate):
        self.login = login
        self.password_hash = password_hash
        self.name = name
        self.active = True
        self.admin = False
        self.hourly_rate = hourly_rate

    def get_current_session(self):
        return object_session(self).query(WorkSession).filter_by(employee_id=self.id, end_time=None).first()

    def close_current_session(self, time=None):
        session = self.get_current_session()
        if session is not None:
            session.close_session(time)


class WorkSession(Base):
    __tablename__ = 'work_session'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    start_time = Column(UTCDateTime, nullable=False)
    end_time = Column(UTCDateTime, nullable=True)
    billing_period_id = Column(Integer, ForeignKey('billing_period.id'), nullable=False)
    hourly_rate = Column(Numeric(precision=6, scale=2), nullable=False)

    employee = relationship('Employee', backref='work_sessions')
    project = relationship('Project', backref='work_sessions')
    billing_period = relationship('BillingPeriod', backref='work_sessions')

    def __init__(self, employee, project, start_time, billing_period):
        self.employee = employee
        self.project = project
        self.start_time = start_time
        self.billing_period = billing_period
        self.hourly_rate = employee.hourly_rate

    def close_session(self, time=None):
        assert(self.end_time is None)
        if time is None:
            tim = util.utcnow()
        self.end_time = time

class BillingPeriod(Base):
    __tablename__ = 'billing_period'
    id = Column(Integer, primary_key=True)
    start_date = Column(UTCDateTime, nullable=False)
    close_date = Column(UTCDateTime, nullable=True)
    description = Column(Text, nullable=False)

    def __init__(self, start_date, description):
        self.start_date = start_date
        self.description = description

    @classmethod
    def get_current(cls):
        return DBSession.query(cls).filter_by(close_date=None).first()
