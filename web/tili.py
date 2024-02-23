from app import create_app, db
from app.models import User, Word, Definition
from flask import request

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 
            'User': User, 
            'Word': Word, 
            'Definition': Definition}
    
BASE_URL = "http://127.0.0.1:5000"
SHUTDOWN = "/shutdown"

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route(SHUTDOWN, methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
    