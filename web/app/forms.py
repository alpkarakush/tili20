from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from app.models import User


class NewWordForm(FlaskForm):
    word_text = StringField('Word', validators=[DataRequired()])
    definition_text = TextAreaField('Definition', validators=[
        DataRequired(), Length(min=1, max=500)])
    example_text = TextAreaField('Example')
    
    nickname = StringField('Nickname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    submit = SubmitField('Submit')

    def validate_nickname(self, nickname):
        nickname_user = User.query.filter_by(nickname=nickname.data).first()
        
        if nickname_user is not None and nickname_user.email != self.email.data:
            # the nickname exists
            raise ValidationError("This nickname already exists")
        