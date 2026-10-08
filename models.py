from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from datetime import date, timedelta
from functools import cache
from typing import Any, Iterable

################################################################################
# This is a custom enum subclass that provides additional methods for 
# working with enums in the context of forms. It allows for easy retrieval of 
# enum members by name or value, and provides a method to get choices suitable 
# for use in form fields.
################################################################################

class FormEnum(Enum):
    '''Custom Enum subclass designed for use with SelectFields in forms.'''
    @classmethod
    @cache
    def get_choices(cls) -> tuple[tuple[str, str], ...]:
        return tuple((member.name, member.value) for member in cls)
    @classmethod
    def get_by_name(cls, name: str) -> FormEnum:
        if name in cls.__members__:
            return cls.__members__[name]
        raise ValueError(f"{name} is not a valid {cls.__name__}")
    @classmethod
    @cache
    def get(cls, entry: Any) -> FormEnum | None:
        '''
           Retrieve an enum member by name or value. 
           If the entry is already a member of the enum, it is returned as-is. 
           If the entry is a string that matches a member name, that member is returned. 
           If the entry matches a member value, that member is returned. 
           If no match is found, a ValueError is raised.
        '''
        # if the entry is already a member of the enum, return it
        if isinstance(entry, cls):
            return entry
        # if the entry is a string and matches a member name, return that member
        if isinstance(entry, str) and entry in cls.__members__:
            return cls.__members__[entry]
        # if the entry matches a member value, return that member
        for member in cls:
            if member.value == entry:
                return member
        # if no match is found, throw an exception
        raise ValueError(f"{entry} is not a valid {cls.__name__}")
    @classmethod
    @cache
    def get_or_default(cls, entry: Any, default: FormEnum | None = None) -> FormEnum | None:
        try:
            return cls.get(entry)
        except ValueError:
            return default
    @classmethod
    @cache
    def get_by_value(cls, value: Any) -> FormEnum:
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"{value} is not a valid {cls.__name__}")

class GameGenre(FormEnum):
    OTHER         =  'Other'
    PARTY         =  'Party'
    PUZZLE        =  'Puzzle'
    RPG           =  'RPG'
    STRATEGY      =  'Strategy'
    COOP          =  'Coop'
    FAMILY        =  'Family'
    DECK_BUILDING =  'Deck Building'
    ADVENTURE     =  'Adventure'
    ABSTRACT      =  'Abstract'
    ECONOMIC      =  'Economic'

@dataclass
class Game:
    id: int
    name: str
    genre: GameGenre
    complexity: int
    min_players: int
    max_players: int
    duration: timedelta
    released: date
    description: str    

class GameCatalog:
    '''A simple in-memory catalog for storing and managing Game instances.'''
    def __init__(self, games: Iterable[Game] | None = None):
        self._games: list[Game] = []
        self._next_id: int = 1
        if games is not None:
            for game in games:
                if not isinstance(game, Game):
                    raise ValueError(f"Invalid game: {game}. Must be an instance of Game.")
                self.add_game(game)
    def add_game(self, game: Game) -> int:
        '''Adds a new game to the catalog and assigns it a unique ID. Returns the assigned ID.'''
        game.id = self._next_id
        self._games.append(game)
        self._next_id += 1
        return game.id
    def get_games(self) -> tuple[Game,...]:
        '''Returns a tuple of all games in the catalog.'''
        return tuple(self._games)
    def get_game_by_id(self, game_id: int) -> Game | None:
        '''Returns the game with the specified ID, or None if no such game exists.'''
        for game in self._games:
            if game.id == game_id:
                return game
        return None

# define some default games for use in testing the application.
# These games will be added to the catalog when the application starts.
default_games: tuple[Game, ...] = (
    Game(
        id=-1, # placeholder that is replaced when added to a game catalog
        name="Catan", 
        genre=GameGenre.STRATEGY, 
        complexity=3, 
        min_players=3, 
        max_players=4, 
        duration=timedelta(minutes=90),
        released=date(1995, 2, 2),
        description="A game of trading and building."
    ),
    Game(
        id=-1, # placeholder that is replaced when added to a game catalog 
        name="Monopoly", 
        genre=GameGenre.ECONOMIC, 
        complexity=2, 
        min_players=2, 
        max_players=6, 
        duration=timedelta(minutes=120), 
        released=date(1935, 11, 5), 
        description="A game of real estate and finance."
    ),
    Game(
        id=-1, # placeholder that is replaced when added to a game catalog 
        name="Pandemic", 
        genre=GameGenre.COOP, 
        complexity=3, 
        min_players=2, 
        max_players=4, 
        duration=timedelta(minutes=45), 
        released=date(2008, 3, 15), 
        description="A cooperative game where players work together to stop global pandemics."
    ),
)
