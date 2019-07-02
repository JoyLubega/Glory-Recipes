from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from Api.api import db, create_app


app = create_app(config_name='DevelopmentEnv')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
