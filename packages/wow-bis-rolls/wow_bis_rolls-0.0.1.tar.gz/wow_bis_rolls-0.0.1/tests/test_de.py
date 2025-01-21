from wow_bis_rolls.rolls import item_was_disenchanted

def test_de_identified():
    item = {"awardedTo": "|de|"}
    test = item_was_disenchanted(item)
    assert  test == True

def test_random_player_not_de():
    item = {"awardedTo": "Gereld"}
    test = item_was_disenchanted(item)
    assert  test == False

def test_weird_characters_not_de():
    item = {"awardedTo": "£$ ^£$T\"  DFGSDFSDV"}
    test = item_was_disenchanted(item)
    assert  test == False
