from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from app.forms import NewWordForm, RegistrationForm, LoginForm
from app.models import User, Word, Definition
from sqlalchemy import cast, Date, func
from flask_login import current_user, login_user, logout_user
from slugify import slugify

@app.route("/register", methods=['post', 'get'])
def register():
    form = RegistrationForm()
    
    # Upon submission
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None and form.nickname.data and form.email.data:
            user = User(nickname=form.nickname.data, 
                        email=form.email.data,
                        consent_to_send_emails= request.form.get('add_word__news'), 
                        consent_to_cookies=request.form.get('add_word__cookie'))
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
        
        flash(f'Жаны соз {form.nickname.data} кошулду!')
        
        return redirect(url_for('index'))
    
    return render_template('user_registration.html', title='Registration', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/delete", methods=['POST'])
def delete():
    data = request.get_json()
    data_id = data['data_id']
    
    definition = Definition.query.get(data_id)
    
    db.session.delete(definition)
    db.session.commit()
    
    app.logger.info('Word is deleted data_id: %s', data_id)
    return f"Deleted {data_id}"


@app.route("/vote", methods=['post'])
def vote():
    data = request.get_json()
    data_id = data['data_id']
    is_upvote = data['is_upvote']
    
    definition = Definition.query.get(data_id)
    if is_upvote:
        definition.upvotes += 1
    else:
        definition.downvotes += 1
    db.session.commit()
    
    app.logger.info('Vote received data_id: %s is_upvote: %s', data_id, is_upvote)
    return "Vote received"

@app.route("/word/<word>", methods=['post', 'get'])
def word(word=None):
    defs = db.session.query(Word, Definition, User,
        ).filter( Word.id == Definition.word_id    
        ).filter( Definition.author_id == User.id
        ).filter( Word.word_text == word  
        ).order_by( Definition.upvotes.desc()
        ).all()
    
    def_list = [ { 'word': d.Word.word_text, 
                  'definition': d.Definition.definition_text, 
                  'example': d.Definition.example_text, 
                  'author': d.User.nickname, 
                  'created_at': d.Definition.created_at.strftime("%d/%m/%Y"), 
                  'upvotes': d.Definition.upvotes, 
                  'downvotes': d.Definition.downvotes,
                  'definition_id': d.Definition.id} 
                        for d in defs ] 
    
    return render_template('word.html', def_list=def_list)


@app.route("/add-new-word", methods=['post', 'get'])
def new_word():
    form = NewWordForm()
    
    # Upon submission
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None and form.nickname.data and form.email.data:
            user = User(nickname=form.nickname.data, 
                        email=form.email.data,
                        consent_to_send_emails= (1 == request.form.get('add_word__news')), 
                        consent_to_cookies=(1 == request.form.get('add_word__cookie')))
            db.session.add(user)
            db.session.commit()
        elif user is None and form.nickname.data is None:
            user = User.query.filter_by(email="anon@mail.com").first()
        
        word = Word.query.filter(Word.word_text.ilike(form.word_text.data)).first()
        if word is None:
            word = Word(form.word_text.data.lower(), 
                        user.id)
            db.session.add(word)
            db.session.commit()
        
        definition = Definition.query.filter(Definition.definition_text.ilike(form.definition_text.data)).first()
        if definition is not None:
            flash('Сөз түшүндүрмөсү базада бар экен!')
            redirect(url_for('index'))
        
        new_definition = Definition(user.id, 
                                    word.id, 
                                    form.definition_text.data, 
                                    form.example_text.data)
        db.session.add(new_definition)
        db.session.commit()
        
        flash(f'Жаны соз {form.word_text.data} кошулду!')
        
        return redirect(url_for('index'))
    
    return render_template('new_word.html', title='Create a new word', form=form)
    

@app.route("/index", methods=['get'])
@app.route("/", methods=['get'])
def index():
    page = request.args.get('page', 1, type=int)
    
    query_result = db.session.query(Word.id, Word.word_text,
                Definition.id, Definition.definition_text, func.max(Definition.created_at), Definition.example_text, 
                Definition.upvotes, Definition.downvotes,
                User.nickname
                ).join(
                    Definition, Definition.word_id == Word.id
                ).join(
                    User, User.id == Definition.author_id
                ).group_by(func.date(Definition.created_at.cast(Date))
                ).paginate(
                    page=page, 
                    per_page=app.config['WORDS_PER_PAGE'], 
                    error_out=False)
    
    words = [ {'word': word[1],
               
               'definition_id': word[2],
               'definition': word[3],
               'created_at': word[4].strftime("%d/%m/%Y"),
               'example': word[5],
               
               'upvotes': word[6],
               'downvotes': word[7],
               
               'author': word[8]
               }  for word in query_result.items]
    
    # Pagination
    next_url = None
    prev_url = None
    
    if query_result.has_next:
        next_url = url_for('index', page=query_result.next_num)
    if query_result.has_prev:
        prev_url = url_for('index', page=query_result.prev_num)
    
    

    return render_template("index.html", 
                           words=words, 
                           next_url=next_url,
                           prev_url=prev_url)
    

@app.route("/favorites", methods=['get'])
def favorites():
    page = request.args.get('page', 1, type=int)
    
    query_result = db.session.query(Word, Definition, User
        ).join(
            Definition, Definition.word_id == Word.id
        ).join(
            User, User.id == Word.author_id
        ).order_by(
            Definition.upvotes.desc()
        ).paginate(
            page=page, 
            per_page=app.config['WORDS_PER_PAGE'], 
            error_out=False)
    
    words = [ {'word': word[0].word_text,
            'definition': word[1].definition_text,
            'example': word[1].example_text,
            'created_at' : word[1].created_at.strftime("%d/%m/%Y"),
            'upvotes': word[1].upvotes,
            'downvotes': word[1].downvotes,
            'author': word[2].nickname}  for word in query_result.items]
    
    # Pagination
    next_url = None
    prev_url = None
    
    if query_result.has_next:
        next_url = url_for('index', page=query_result.next_num)
    if query_result.has_prev:
        prev_url = url_for('index', page=query_result.prev_num)

    return render_template("favorites.html", 
                           words=words, 
                           next_url=next_url,
                           prev_url=prev_url)

@app.route("/newly-added", methods=['get'])
def newly_added():
    page = request.args.get('page', 1, type=int)
    
    query_result = db.session.query(Word, Definition, User
        ).join(
            Definition, Definition.word_id == Word.id
        ).join(
            User, User.id == Word.author_id
        ).order_by(
            Word.created_at.desc()
        ).paginate(
            page=page, 
            per_page=app.config['WORDS_PER_PAGE'], 
            error_out=False)
    
    words = [ {'word': word[0].word_text,
            'definition': word[1].definition_text,
            'example': word[1].example_text,
            'created_at' : word[1].created_at.strftime("%d/%m/%Y"),
            'upvotes': word[1].upvotes,
            'downvotes': word[1].downvotes,
            'author': word[2].nickname}  for word in query_result.items]
    
    # Pagination
    next_url = None
    prev_url = None
    
    if query_result.has_next:
        next_url = url_for('index', page=query_result.next_num)
    if query_result.has_prev:
        prev_url = url_for('index', page=query_result.prev_num)

    return render_template("newly_added.html", 
                           words=words, 
                           next_url=next_url,
                           prev_url=prev_url)