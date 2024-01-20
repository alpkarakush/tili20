# Tili 2.0 - Urban dictionary of kyrgyz

## Instructions:
- git clone https://github.com/alpkarakush/tili20.git
- export FLASK_APP=path_to_folder/tili20/web
- flask run

## DB:
- words (word_id, word_text, created_at, author(user_id))
- definitions(word(word_id), description_text, created_at, upvotes, downvotes)
- users(user_id, nickname)

Steps to initiate:
- flask db init
- flask db migrate
- flask db upgrade

## How to run in debug mode
1. Create a file launch.json in .vscode folder
```
{
    "python.condaPath": "/path-to/anaconda",
    "version": "0.2.0",
    "configurations": [

        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env" : {
                "FLASK_APP": "tili.py",
                "FLASK_ENV": "development"
            },
            "cwd" : "/path-to/tili20/web",
            "args": [
                "run",
                "--debugger"
            ]
        }
    ]
}
```
2. Read this [source](https://code.visualstudio.com/docs/python/tutorial-flask#:~:text=Select%20the%20link%20and%20VS,object%20within%20the%20configuration%20array.) for further steps. 

## How to deploy
1. Pull the code to server
2. Install requiements.txt
3. Assign environment variables
   1. SECRET_KEY

## Todo:
There are many imporvements to make to this website. Feel free to send PRs and be a part of Neo-Kyrgyz movement.


* [ ] Add admin panel for managing words
* [ ] Limit per user words at 5 a day
* [ ] Add caching for index page
* [ ] Prepare prod and debug configs and corresponding environments
* [ ] Write tests
* [ ] Prepare CI & CD
* [ ] Make a full-text search
* [ ] Make a word page to show all definitions of given word
* [ ] Make prettier logo
* [ ] Customize website design
* [ ] Add aching for pages
  * [ ] Don't forget to force update upon adding new word
* [ ] Make a created_at date more like whatsapp messages (added 8 minutes ago, ...) 
* [ ] Add authors pages and make authors nickname clickable in word section
* [ ] Add share button
  * [ ] Export in pretty image format
  * [ ] Add text-to-speech
* [ ] Make a script scraping often used words, that are not in dictionary
  * [ ] It might scape news portals, but they often use formal language
  * [ ] Try to make a scraper that pulls instagram/tik-tok comments, which often contain informal language
* [ ] Make a page to fill in words for volunteers
* [ ] Make a bot that posts Word of the day on social media with pretty image formating



