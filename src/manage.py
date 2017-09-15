#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
if os.path.exists('.env'):
    # print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

mc = MigrateCommand
manager.add_command('db', mc)

from manage_mercadopublico import MPCommand
manager.add_command('mp', MPCommand)

# from manage_test import TestCommand
# manager.add_command('test', TestCommand)


@mc.command
def drop_all(reflect=False):
    """
    Custom drop_all
    """
    if reflect:
        db.reflect()
    db.drop_all()


@mc.command
def create_all():
    """
    Create all from sqlalchemy db
    """
    db.create_all()


if __name__ == '__main__':
    manager.run()

