import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand

from application import create_app, db

app = create_app()
app.app_context().push()
manager = Manager(app)

manager.add_command("runserver",Server(
    use_debugger=True,
    use_reloader=True
))



migrate = Migrate(app, db)


manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()