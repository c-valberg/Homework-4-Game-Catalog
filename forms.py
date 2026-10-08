from __future__ import annotations

from datetime import date
from pathlib import Path
import sys

from flask_wtf import FlaskForm
from wtforms import (
    FormField, StringField, SelectField, IntegerField, DateField, TextAreaField, SubmitField
)
from wtforms.widgets import RangeInput
from wtforms.validators import InputRequired, NumberRange, Length, ValidationError, Optional

# ensure that this script's directory is in the sys.path so that we can import from models.py
script_dir = Path(__file__).resolve().parent
if str(script_dir) not in sys.path:
    sys.path.append(str(script_dir))

from models import GameGenre

# TODO: Implement any custom validators you need

class GameForm(FlaskForm):
    # TODO: Implement your form class
    pass
