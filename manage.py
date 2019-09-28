import os, sys
import datetime 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand

from application import create_app, db

app = create_app()
app.app_context().push()
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
manager.add_command("runserver",Server(
    use_debugger=True,
    use_reloader=True
))

@app.context_processor
def inject_now():
    return {'now': datetime.datetime.utcnow()}


if __name__ == '__main__':
    manager.run()