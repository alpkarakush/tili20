
from flask import render_template, flash, redirect, url_for, request, jsonify, current_app, send_from_directory
from collections import namedtuple
from app.main.forms import NewWordForm
from app.models import User, Word, Definition
from sqlalchemy import cast, Date, func
from app import db
from app.main import bp
import os

@bp.route("/delete", methods=['POST'])
def delete():
    data = request.get_json()
    data_id = data['data_id']
    
    definition = Definition.query.get(data_id)
    
    db.session.delete(definition)
    db.session.commit()
    
    current_app.logger.info('Word is deleted data_id: %s', data_id)
    return f"Deleted {data_id}"

@bp.route("/vote", methods=['post'])
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
    
    current_app.logger.info('Vote received data_id: %s is_upvote: %s', data_id, is_upvote)
    return "Vote received"

@bp.route("/word/<word>", methods=['post', 'get'])
def word(word=None):
    if not word:
        return "Word parameter is missing", 400
    
    results = (
        db.session.query(
            Word.word_text,
            Definition.definition_text,
            Definition.example_text,
            User.nickname,
            Definition.created_at,
            Definition.upvotes,
            Definition.downvotes,
            Definition.id
        )
        .select_from(Word)
        .join(Definition, Word.id == Definition.word_id)
        .join(User, Definition.author_id == User.id)
        .filter(Word.word_text == word)
        .order_by(Definition.upvotes.desc())
        .all()
    )
    
    def_list = [
        {
            'word': result.word_text,
            'definition': result.definition_text,
            'example': result.example_text,
            'author': result.nickname,
            'created_at': result.created_at.strftime("%d/%m/%Y"),
            'upvotes': result.upvotes,
            'downvotes': result.downvotes,
            'definition_id': result.id
        }
        for result in results
    ]
    
    return render_template('word.html', def_list=def_list)

@bp.route("/add-new-word", methods=['post', 'get'])
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
            redirect(url_for('main.index'))
        
        new_definition = Definition(user.id, 
                                    word.id, 
                                    form.definition_text.data, 
                                    form.example_text.data)
        db.session.add(new_definition)
        db.session.commit()
        
        flash(f'Жаны соз {form.word_text.data} кошулду!')
        
        return redirect(url_for('main.index'))
    
    return render_template('new_word.html', title='Create a new word', form=form)

@bp.route("/index", methods=['get'])
@bp.route("/", methods=['get'])
def index():
    page = request.args.get('page', 1, type=int)
    
    query_result = (
        db.session.query(Word, Definition, User)
        .join(Definition, Definition.word_id == Word.id)
        .join(User, User.id == Word.author_id)
        .order_by(Word.created_at.desc())
        .paginate(page=page, per_page=current_app.config['WORDS_PER_PAGE'], error_out=False)
    )

    words = [
        {
            'word': word.word_text,
            'definition': definition.definition_text,
            'definition_id': definition.id,
            'example': definition.example_text,
            'created_at': definition.created_at.strftime("%d/%m/%Y"),
            'upvotes': definition.upvotes,
            'downvotes': definition.downvotes,
            'author': user.nickname
        }
        for word, definition, user in query_result.items
    ]

    # Extract next and previous page URLs
    next_url = url_for('main.index', page=query_result.next_num) if query_result.has_next else None
    prev_url = url_for('main.index', page=query_result.prev_num) if query_result.has_prev else None

    # Render the template with the data
    return render_template("index.html", 
                        words=words, 
                        next_url=next_url,
                        prev_url=prev_url)

@bp.route("/favorites", methods=['get'])
def favorites():
    page = request.args.get('page', 1, type=int)

    query_result = (
        db.session.query(Word, Definition, User)
        .join(Definition, Definition.word_id == Word.id)
        .join(User, User.id == Word.author_id)
        .order_by(Definition.upvotes.desc())
        .paginate(page=page, per_page=current_app.config['WORDS_PER_PAGE'], error_out=False)
    )

    words = [
        {
            'word': word.word_text,
            'definition': definition.definition_text,
            'definition_id': definition.id,
            'example': definition.example_text,
            'created_at': definition.created_at.strftime("%d/%m/%Y"),
            'upvotes': definition.upvotes,
            'downvotes': definition.downvotes,
            'author': user.nickname
        }
        for word, definition, user in query_result.items
    ]

    next_url = url_for('main.favorites', page=query_result.next_num) if query_result.has_next else None
    prev_url = url_for('main.favorites', page=query_result.prev_num) if query_result.has_prev else None

    return render_template("favorites.html", words=words, next_url=next_url, prev_url=prev_url)

@bp.route("/newly-added", methods=['GET'])
def newly_added():
    page = request.args.get('page', 1, type=int)

    query_result = (
        db.session.query(Word, Definition, User)
        .join(Definition, Definition.word_id == Word.id)
        .join(User, User.id == Word.author_id)
        .order_by(Word.created_at.desc())
        .paginate(page=page, per_page=current_app.config['WORDS_PER_PAGE'], error_out=False)
    )

    words = [
        {
            'word': word.word_text,
            'definition': definition.definition_text,
            'definition_id': definition.id,
            'example': definition.example_text,
            'created_at': definition.created_at.strftime("%d/%m/%Y"),
            'upvotes': definition.upvotes,
            'downvotes': definition.downvotes,
            'author': user.nickname
        }
        for word, definition, user in query_result.items
    ]

    next_url = url_for('main.newly_added', page=query_result.next_num) if query_result.has_next else None
    prev_url = url_for('main.newly_added', page=query_result.prev_num) if query_result.has_prev else None

    return render_template("newly_added.html", words=words, next_url=next_url, prev_url=prev_url)

@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
