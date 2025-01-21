import pytest
from wow_bis_rolls.rolls import get_winning_roll 

test_item = {
    "itemLink": "itemname",
    "Rolls":[
        {"player":"player0"},
        {"player":"player1"},
        {"player":"player7"},
    ]
}

def test_player1_winner():
    winner = "player0"
    winning_roll = get_winning_roll(test_item, winner)
    assert winning_roll["player"] == "player0"

def test_winner_missing():
    winner = "does not exist"
    with pytest.raises(ValueError):
        winning_roll = get_winning_roll(test_item, winner)