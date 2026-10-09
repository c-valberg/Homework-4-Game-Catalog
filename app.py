from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
import sys
from typing import cast

from flask import Flask, render_template, redirect, url_for, flash

# add the current directory to the path so that we can import from models.py and forms.py
script_dir = Path(__file__).resolve().parent
if str(script_dir) not in sys.path:
    sys.path.append(str(script_dir))

# import the necessary classes from models.py and forms.py
from models import GameCatalog, GameGenre, Game, default_games
from forms import GameForm

app = Flask(__name__)
app.secret_key = 'EngineerUseSimplicityIntoPresenceOrnament'

# Your in-memory games catalog
catalog = GameCatalog(games=default_games)

@app.route('/')
def index():
    return redirect(url_for('get_games'))

@app.get('/games')
def get_games():
    form: GameForm = GameForm()
    return render_template('game_catalog.html', games=catalog.get_games(), form=form)

@app.post('/games')
def post_game():
    form: GameForm = GameForm()
    if form.validate_on_submit():
        game = Game(
            id=-1,  # placeholder, replaced by catalog.add_game
            name=form.name.data.strip(),
            genre=GameGenre.get(form.genre.data),
            complexity=form.complexity.data,
            min_players=form.min_players.data,
            max_players=form.max_players.data,
            duration=timedelta(minutes=form.playtime.data),  # form is in minutes, model uses timedelta
            released=form.release_date.data,                 # None if left blank; template guards it
            description=form.description.data or '',
        )
        catalog.add_game(game)
        flash(f'Added "{game.name}" to the catalog!', 'success')
        return redirect(url_for('get_games'))  # Post/Redirect/Get

    flash('Please correct the errors in the form.', 'error')
    return render_template('game_catalog.html', games=catalog.get_games(), form=form), 422