from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import NewWordForm
from app.models import User, Word, Definition


@app.route("/new_word", methods=['post', 'get'])
def new_word():
    form = NewWordForm()
    
    if form.validate_on_submit():
        flash(f'A new word {form.word_text} has been added.')
        
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(form.nickname.data, form.email.data)
            db.session.add(user)
            db.session.commit()
        
        word = Word.query.filter_by(word_text=form.word_text.data).first()
        if word is None:
            word = Word(form.word_text.data, user.id)
            db.session.add(word)
            db.session.commit()
        
        definition = Definition.query.filter_by(definition_text=form.definition_text.data).first()
        if definition is not None:
            flash('Definition already exists!')
            redirect(url_for('index'))
        
        new_definition = Definition(user.id, word.id, form.definition_text.data, form.example_text.data)
        db.session.add(new_definition)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('new_word.html', title='Create a new word', form=form)

@app.route("/index", methods=['get'])
@app.route("/", methods=['get'])
def index():
    page = request.args.get('page', 1, type=int)
    words = Word.query.order_by(Word.created_at.desc()).paginate(
        page, app.config['WORDS_PER_PAGE'], False)
    
    query_result = db.session.query(Word, Definition, User
        ).join(
            Definition, Definition.word_id == Word.id
        ).join(
            User, User.id == Word.author_id
        ).order_by(
            Word.created_at.desc()
        ).paginate(
            page, app.config['WORDS_PER_PAGE'], False).items
    
    words = [ {'word': word[0].word_text, 
               'definition': word[1].definition_text, 
               'example': word[1].example_text, 
               'author': word[2].nickname}  for word in query_result]

    return render_template("index.html", words=words)