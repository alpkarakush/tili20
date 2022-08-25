# Tili 2.0 - Urban dictionary of kyrgyz

## Instructions:
- git clone https://github.com/alpkarakush/tili20.git
- export FLASK_APP=path_to_folder/tili20/web
- flask run

## DB:
- words (word_id, word_text, created_at, author(user_id))
- definitions(word(word_id), description_text, created_at)
- users(user_id, nickname)

flask db init
flask db migrate
flask db upgrade

