from app import db
from datetime import datetime
from flask_login import UserMixin
from app import login
from werkzeug.security import check_password_hash, generate_password_hash
import sqlalchemy.orm as so
import sqlalchemy as sa
from typing import Optional


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    verified = db.Column(db.Boolean, index=True, default=False)
    consent_to_send_emails = db.Column(db.Boolean, index=True, default=False)
    consent_to_cookies = db.Column(db.Boolean, index=True, default=False)
    password_hash = db.Column(db.String(256))
    
    words = db.relationship('Word', backref='author', lazy='dynamic')
    
    def __init__(self, nickname, email, consent_to_send_emails=False, consent_to_cookies=False):
        self.nickname = nickname
        self.email = email
    
    def verify(self):
        self.verified = True
    
    def __repr__(self):
        return '<User %r>' % self.nickname
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_text = db.Column(db.String(80), index=True, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    definitions = db.relationship('Definition', backref='parent_word', lazy='dynamic')
    
    def __init__(self, word_text, author_id):
        self.word_text = word_text
        self.author_id = author_id

    
    def __repr__(self):
        return '<Word %r>' % self.word_text

class Definition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    definition_text = db.Column(db.String(300), nullable=False)
    example_text = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    upvotes = db.Column(db.Integer, nullable=False, default=0)
    downvotes = db.Column(db.Integer, nullable=False, default=0)
    
    word_id = db.Column(db.Integer, db.ForeignKey("word.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    def __init__(self, author_id, word_id, definition_text=None, example_text=None):
        self.definition_text = definition_text
        self.example_text = example_text
        self.author_id = author_id
        self.word_id = word_id
    
    def upvote(self):
        self.upvotes += 1
    def unupvote(self):
        self.upvotes -= 1
    def downvote(self):
        self.downvotes += 1
    def undownvote(self):
        self.downvotes -= 1
    
    def __repr__(self):
        return '<Definition %r>' % self.definition_text
