from wow_bis_rolls.rolls import roll_was_bis

def test_bis_roll_true():
    roll = {"classification": "BiS"}
    test = roll_was_bis(roll)
    assert  test == True

def test_ms_roll_false():
    roll = {"classification": "MS"}
    test = roll_was_bis(roll)
    assert  test == False

def test_os_roll_false():
    roll = {"classification": "OS"}
    test = roll_was_bis(roll)
    assert  test == False