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
    raise NotImplementedError("TODO: Implement this function!")
