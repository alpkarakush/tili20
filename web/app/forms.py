from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo
from app.models import User


class NewWordForm(FlaskForm):
    word_text = StringField('Сөз', validators=[DataRequired(message="Cөздү жазыныз")])
    definition_text = TextAreaField('Түшүндүрмө', validators=[DataRequired(message="Түшүндүрмө кошуу зарыл"), Length(min=1, max=500)])
    example_text = TextAreaField('Мисал')
    
    nickname = StringField('Лакап/Атынар')
    email = StringField('Имейл', validators=[Email()])
    receive_emails = BooleanField('receive_emails')
    allow_cookies = BooleanField('allow_cookies')
    submit = SubmitField('Жөнөт')
    
    def validate_nickname(self, nickname):
        nickname_user = User.query.filter_by(nickname=nickname.data).first()
        
        if nickname_user is not None and nickname_user.email != self.email.data:
            # the nickname exists
            raise ValidationError("This nickname already exists")

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
