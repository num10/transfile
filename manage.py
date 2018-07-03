#!/usr/bin/ python
# -*- coding: UTF-8 -*-

import os
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Role
from flask_uploads import configure_uploads
from app.auth.forms import pdfs,photos,words

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
configure_uploads(app, pdfs)
configure_uploads(app, photos)
configure_uploads(app, words)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    app.run()