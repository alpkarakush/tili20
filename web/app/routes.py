from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import NewWordForm
from app.models import User, Word, Definition
from sqlalchemy import cast, Date, func

@app.before_request
def limit_remote_addr():
    if request.script_root == '/admin' and request.remote_addr != os.environ.get('ADMIN_REMOTE_IP'):
        abort(403)


@app.route("/admin", methods=['post'])
def admin():
    return "hello"



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
    return f"The word is {word}"


@app.route("/new_word", methods=['post', 'get'])
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
                    User, User.id == Word.author_id
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

@app.route("/newly_added", methods=['get'])
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