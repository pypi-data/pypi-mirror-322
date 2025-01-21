import pathlib
from wow_bis_rolls.rolls import parse_file_for_bis_rolls, read_json

TESTFILE = pathlib.Path(__file__).parent / "rolls.json"

def test_read_json():
    """Verify that the file reads without issue"""
    read_json(TESTFILE)

def test_full_run(capsys):
    """Test a full run matches the sample output"""
    parse_file_for_bis_rolls(TESTFILE)
    captured = capsys.readouterr()
    assert captured.out == """Wartorious won BiS on [Dark Edge of Insanity]
Angelnomore won BiS on [Dark Storm Gauntlets]
Byornski won BiS on [Carapace of the Old God]
Kongtikki won BiS on [Husk of the Old God]
Freewrath won BiS on [Husk of the Old God]
Tornwulf won BiS on [Intact Viscera]
Iskhiaro won BiS on [Intact Peritoneum]
Inarra won BiS on [Intact Entrails]
"""
    

