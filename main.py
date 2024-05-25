from flask import Flask, render_template, request, make_response
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session
import random

from models import Genre, Song, User

engine = create_engine('sqlite:///myDatabase.db', echo=True)

app = Flask(__name__)

def validateForm(user):
    if len(user.name) == 0:
        return False
    if len(user.password) == 0:
        return False
    return True


@app.route('/', methods=['POST', 'GET'])
def index():
    log = ""
    if request.cookies.get('logged'):
        log = request.cookies.get('logged')
    with Session(engine) as session:
        genres = list(session.query(Genre).order_by(Genre.genre))
        if request.method == 'POST' and log == 'yes':  # log out
            res = make_response(render_template('main-page.html', genres=genres, log='no', name='noName'))
            res.set_cookie('logged', 'no', 0)
            res.set_cookie('name', '', 0)
            return res
        elif request.method == 'POST' and log != 'yes':  # log in
            user = list(session.query(User).where(User.name == request.form['login']))
            if len(user) > 0:  # user with this login exists
                user = user[0]
                if request.form['password'] == user.password:
                    res = make_response(render_template('main-page.html', genres=genres, log='yes', name=user.name))
                    res.set_cookie('logged', 'yes', 3600)
                    res.set_cookie('name', user.name, 3600)
                    return res
                else:  # wrong password
                    return render_template('main-page.html', genres=genres, log='no', name='noName')
            else:  # no such user -> let`s make it
                newUser = User(
                    name=request.form['login'],
                    password=request.form['password']
                )
                if validateForm(newUser) == False:
                    return render_template('main-page.html', genres=genres, log='no', name='noName')
                session.add(newUser)
                session.commit()
                res = make_response(render_template('main-page.html', genres=genres, log='yes', name=newUser.name))
                res.set_cookie('logged', 'yes', 3600)
                res.set_cookie('name', newUser.name, 3600)
                return res

    if request.method == 'GET' and log == 'yes':
        name = request.cookies.get('name')
        res = make_response(render_template('main-page.html', genres=genres, log='yes', name=name))
        return res
    elif request.method == 'GET' and log != 'yes':
        res = make_response(render_template('main-page.html', genres=genres, log='no', name='noName'))
        res.set_cookie('logged', '', 0)
        res.set_cookie('name', '', 0)
        return res


@app.route('/audio_mode/<genre_id>')
def audio_mode(genre_id):
    with Session(engine) as session:
        genre = session.query(Genre).where(Genre.id == genre_id).first()
        randomSongs = list(session.query(Song).where(Song.genre == genre.id).order_by(func.random()).limit(4))
    rightSong = randomSongs[0]
    random.shuffle(randomSongs)
    rightIndex = randomSongs.index(rightSong)
    return render_template('audio-mode.html', rightSong=rightSong, genre=genre, randomSongs=randomSongs,
                           rightIndex=rightIndex)


@app.route('/text_mode/<genre_id>')
def text_mode(genre_id):
    with Session(engine) as session:
        genre = session.query(Genre).where(Genre.id == genre_id).first()
        randomSongs = list(session.query(Song).where(Song.genre == genre.id).order_by(func.random()).limit(4))
    rightSong = randomSongs[0]
    random.shuffle(randomSongs)
    rightIndex = randomSongs.index(rightSong)
    return render_template('text-mode.html', rightSong=rightSong, genre=genre, randomSongs=randomSongs,
                           rightIndex=rightIndex)


if __name__ == '__main__':
    app.run(debug=True)
