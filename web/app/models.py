from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    verified = db.Column(db.Boolean, index=True, default=False)
    
    words = db.relationship('Word', backref='author', lazy='dynamic')
    
    def __init__(self, nickname, email):
        self.nickname = nickname
        self.email = email
    
    def verify(self):
        self.verified = True
    
    def __repr__(self):
        return '<User %r>' % self.nickname

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_text = db.Column(db.String(80), index=True, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    upvotes = db.Column(db.Integer, nullable=True, default=0)
    downvotes = db.Column(db.Integer, nullable=True, default=0)
    
    definitions = db.relationship('Definition', backref='parent_word', lazy='dynamic')
    
    def __init__(self, word_text, author_id):
        self.word_text = word_text
        self.author_id = author_id
    
    def upvote(self):
        self.upvotes += 1
    def unupvote(self):
        self.upvotes -= 1
    
    def downvote(self):
        self.downvotes += 1
    def undownvote(self):
        self.downvotes -= 1
    
    def __repr__(self):
        return '<Word %r>' % self.word_text

class Definition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    definition_text = db.Column(db.String(300), nullable=False)
    example_text = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    word_id = db.Column(db.Integer, db.ForeignKey("word.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    def __init__(self, author_id, word_id, definition_text=None, example_text=None):
        self.definition_text = definition_text
        self.example_text = example_text
        self.author_id = author_id
        self.word_id = word_id
    
    def __repr__(self):
        return '<Definition %r>' % self.definition_text
