from app import login
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request

class DefinitionView(ModelView):
    can_delete = True  # disable model deletion
    page_size = 50  # the number of entries to display on the list view
    edit_modal = True
    create_modal = True    
    can_export = True
    can_view_details = True
    details_modal = True
    
class AdminView(ModelView):
    can_delete = True  # disable model deletion
    page_size = 50  # the number of entries to display on the list view

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))