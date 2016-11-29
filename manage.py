import flask_script

from app import app


manager = flask_script.Manager(app, with_default_commands=False)

@manager.command
def run():
    """Run the endpoint locally in the debug server"""
    app.run(debug=True, host='0.0.0.0')


if __name__ == '__main__':
    manager.run()
