import pytest
from game import Game

def test_get_room_prompt(game):
    prompt = game.get_room_prompt()
    assert prompt is not None

def test_select_object(game):
    game.select_object(0)
    assert game.attempts == 0

def test_guess_code(game):
    result = game.guess_code(456)
    assert result is True
    result = game.guess_code(789)
    assert result is False
    
def test_check_code(game):
    assert game.room.check_code(456) is True
    assert game.room.check_code(123) is False
    
def test_get_game_object_names(game):
    object_names = game.room.get_game_object_names()
    assert len(object_names) == 5
    for object in object_names:
        assert isinstance(object, str)
        assert object is not None

@pytest.fixture
def game():
    return Game()
