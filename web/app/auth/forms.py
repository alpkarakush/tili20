from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo

class RegistrationForm(FlaskForm):
    nickname = StringField('Лакап/Атынар', validators=[DataRequired()])
    email = StringField('Имейл', validators=[DataRequired(), Email()])
    password = PasswordField('Сыр сөз', [DataRequired("Сыр сөздү жазыныз"), Length(min=5)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    receive_emails = BooleanField('receive_emails')
    submit = SubmitField('Жөнөт')
    
    def validate_nickname(self, nickname):
        nickname_user = User.query.filter_by(nickname=nickname.data).first()
        
        if nickname_user is not None and nickname_user.email != self.email.data:
            # the nickname exists
            raise ValidationError("This nickname already exists")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')