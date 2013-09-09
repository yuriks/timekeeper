from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
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

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    login = Column(Text, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    active = Column(Boolean, nullable=False)
    admin = Column(Boolean, nullable=False)

    def __init__(self, login, password_hash, name):
        self.login = login
        self.password_hash = password_hash
        self.name = name
        self.active = True
        self.admin = False

    def get_current_session(self):
        return object_session(self).query(WorkSession).filter_by(employee_id=self.id, end_time=None).first()

class WorkSession(Base):
    __tablename__ = 'work_session'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    billing_period_id = Column(Integer, ForeignKey('billing_period.id'), nullable=False)

    employee = relationship('Employee', backref='work_sessions')
    project = relationship('Project', backref='work_sessions')
    billing_period = relationship('BillingPeriod', backref='work_sessions')

    def __init__(self, project):
        self.projet = project

class BillingPeriod(Base):
    __tablename__ = 'billing_period'
    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime, nullable=False)
    close_date = Column(DateTime, nullable=True)
    description = Column(Text, nullable=False)

    def __init__(self, start_date, description):
        self.start_date = start_date
        self.description = description
