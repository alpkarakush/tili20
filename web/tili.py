from app import db, app
from app.models import User, Word, Definition



@app.shell_context_processor
def make_shell_context():
    return {'db': db, 
            'User': User, 
            'Word': Word, 
            'Definition': Definition}
    
