import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    Base,
    Project,
    BillingPeriod,
    Employee,
    )

from ..security import (
        generate_user_password,
        )

from .. import util


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        project = Project(name="other", description="Work outside of a registered project.")
        period = BillingPeriod(start_date=util.utcnow(), description="")
        admin = Employee(login='admin',
                         password_hash=generate_user_password('timekeeper'),
                         name="Administrator",
                         hourly_rate=0)
        admin.admin = True
        DBSession.add(project)
        DBSession.add(period)
        DBSession.add(admin)
