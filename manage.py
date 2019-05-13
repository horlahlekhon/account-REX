from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask import Flask
from project.app.models import User
from project.app import database, app

migrate = Migrate(app,database)

manager = Manager(app)

manager.add_command('database', MigrateCommand)


@manager.command
def create_db():
    database.create_all()

@manager.command
def drop_db():
    database.drop_all()


if __name__ == "__main__":
    manager.run()