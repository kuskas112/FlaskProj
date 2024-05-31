from flask import Flask, render_template, request, make_response, jsonify
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
                    password=request.form['password'],
                    wins=0,
                    loses=0
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


@app.route('/game_result/<result>')
def game_result(result):
    wins = int(request.cookies.get('wins'))
    response = make_response()
    if result == 'win':
        response.set_cookie('wins', str(wins + 1), 3600)
    else:
        response.set_cookie('wins', str(wins), 3600)
    return response

@app.route('/songs/<genre_id>')
def get_songs(genre_id):
    with Session(engine) as session:
        genre = session.query(Genre).where(Genre.id == genre_id).first()
        randomSongs = list(session.query(Song).where(Song.genre == genre.id).order_by(func.random()).limit(10))
        randomSongs = [{'path': x.pathMusic, 'author': x.author, 'name': x.songName} for x in randomSongs]
        return jsonify(randomSongs)

@app.route('/tiles/<genre_id>')
def get_tiles(genre_id):
    with Session(engine) as session:
        genre = session.query(Genre).where(Genre.id == genre_id).first()
        randomSongs = list(session.query(Song).where(Song.genre == genre.id).order_by(func.random()).limit(4))
        randomSongs = [{'path': x.pathMusic, 'author': x.author, 'name': x.songName} for x in randomSongs]
        return jsonify(randomSongs)



@app.route('/game/<mode>/<genre_id>/<int:songInd>')
def game(mode,genre_id, songInd):
    with Session(engine) as session:
        genre = session.query(Genre).where(Genre.id == genre_id).first()
        randomSongs = list(session.query(Song).where(Song.genre == genre.id).order_by(func.random()).limit(4))
        songsId = ''
        allSongs = []
        if songInd == 0:
            allSongs = list(session.query(Song).where(Song.genre == genre.id).order_by(func.random()).limit(10))
            for song in allSongs:
                songsId += str(song.id) + ','
        elif songInd == 10:
            wins = int(request.cookies.get('wins'))
            userName = 'Unlogged'
            totalWinRate = 0
            if wins == 10:
                totalWinRate = 100
            else:
                totalWinRate = wins / (wins + (10 - wins)) * 100
            if request.cookies.get('logged'):
                user = session.query(User).where(User.name == request.cookies.get('name')).first()
                user.wins += wins
                user.loses += 10 - wins
                session.commit()
                userName = user.name
                if user.loses == 0:
                    totalWinRate = 100
                else:
                    totalWinRate = user.wins / (user.loses + user.wins) * 100
            responce = make_response(
                render_template('end.html', wins=wins, userName=userName, totalWinRate=totalWinRate))
            responce.set_cookie('songsId', '-1', 0)
            return responce
        else:
            songsId = request.cookies.get('songsId')
            songsId = songsId[:-1]
            IDs = songsId.split(',')
            for id in IDs:
                allSongs.append(session.query(Song).where(Song.id == id).first())
        rightSong = allSongs[songInd]
        random.shuffle(randomSongs)
        rightIndex = None
        if rightSong in randomSongs:
            rightIndex = randomSongs.index(rightSong)
        else:
            rightIndex = random.randint(0, 3)
            randomSongs[rightIndex] = rightSong

        template = ''
        if mode == 'audio_mode':
            template = 'audio-mode.html'
        elif mode == 'text_mode':
            template = 'text-mode.html'
        else:
            template = 'main-page.html'

        responce = make_response(
            render_template(template, rightSong=rightSong, genre=genre, randomSongs=randomSongs,
                            rightIndex=rightIndex, songInd=songInd))
        if songInd == 0:
            responce.set_cookie('wins', '0', 3600)
            responce.set_cookie('songsId', songsId, 3600)
        return responce


if __name__ == '__main__':
    app.run(debug=True)
