from app import db
from app.models import User, Definition, Word
from app.admin.views import AdminView
from admin_blueprint import AdminBlueprint

app = AdminBlueprint('admin2', __name__,url_prefix='/admin2',static_folder='static', static_url_path='/static/admin')
app.add_view(AdminView(User, db.session))
app.add_view(AdminView(Definition, db.session))
app.add_view(AdminView(Word, db.session))