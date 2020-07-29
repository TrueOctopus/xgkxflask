import os
from app import create_app, db
from flask_migrate import Migrate, MigrateCommand
from app.models import User
from flask_script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)


manager.add_command("shell", Shell(make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    app.run()
