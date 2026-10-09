from __future__ import annotations

from datetime import date
from pathlib import Path
import sys

from flask_wtf import FlaskForm
from wtforms import (
    FormField, StringField, SelectField, IntegerField, DateField, TextAreaField, SubmitField
)
from wtforms.widgets import RangeInput
from wtforms.validators import (
    DataRequired, InputRequired, NumberRange, Length, Optional, ValidationError
)
# ensure that this script's directory is in the sys.path so that we can import from models.py
script_dir = Path(__file__).resolve().parent
if str(script_dir) not in sys.path:
    sys.path.append(str(script_dir))

from models import GameGenre

class LessThanOrEqualTo:
    """Field's value must not exceed the value of another field in the same form."""

    def __init__(self, other_name: str, message: str | None = None):
        self.other_name = other_name
        self.message = message

    def __call__(self, form, field):
        other = form[self.other_name]
        # if either value is missing/invalid, the other validators report it
        if field.data is None or other.data is None:
            return
        if field.data > other.data:
            raise ValidationError(
                self.message or f'Must be less than or equal to {other.label.text}.'
            )


def not_in_future(form, field):
    """Reject dates after today. Runs only for non-empty input because of Optional()."""
    if field.data is not None and field.data > date.today():
        raise ValidationError('Release date cannot be in the future.')


class GameForm(FlaskForm):
    # Max of 100: the longest real board game titles are well under this, and it
    # keeps the catalog display from breaking on absurdly long input.
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])

    genre = SelectField(
    'Genre',
    choices=[('', 'Select a genre...'), *GameGenre.get_choices()],
    validators=[InputRequired()],
    )

    # min/max are passed as HTML attributes via render_kw, not to the widget itself
    complexity = IntegerField(
        'Complexity',
        widget=RangeInput(step=1),
        default=3,
        render_kw={'min': 1, 'max': 5},
        validators=[InputRequired(), NumberRange(min=1, max=5)],
    )

    min_players = IntegerField('Min Players', validators=[
        InputRequired(), NumberRange(min=1, max=99), LessThanOrEqualTo('max_players'),
    ])
    max_players = IntegerField('Max Players', validators=[
        InputRequired(), NumberRange(min=1, max=99),
    ])

    playtime = IntegerField('Playtime (minutes)', validators=[
        InputRequired(), NumberRange(min=1, max=1440),
    ])

    release_date = DateField('Release Date', validators=[Optional(), not_in_future])

    description = TextAreaField('Description', validators=[Optional(), Length(max=10000)])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # computed per form instance (not at import time) so it never goes stale;
        # makes the browser's date picker block future dates
        self.release_date.render_kw = {'max': date.today().isoformat()}