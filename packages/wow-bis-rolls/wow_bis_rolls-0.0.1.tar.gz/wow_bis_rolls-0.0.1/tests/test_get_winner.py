from wow_bis_rolls.rolls import get_winner

def test_disenchant_winner():
    item = {"awardedTo": "|de|"}
    test = get_winner(item)
    assert  test == "|de|"

def test_random_player_winner():
    item = {"awardedTo": "Gereld"}
    test = get_winner(item)
    assert  test == "Gereld"

def test_server_name_removed_winner():
    item = {"awardedTo": "Gereld-WildGrowth"}
    test = get_winner(item)
    assert  test == "Gereld"

