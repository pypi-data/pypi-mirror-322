import argparse
import json


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        prog="wow-bis-rolls",
        description="Finds all the BiS(101) rolls in a gargul json file",
    )
    parser.add_argument("filename")
    return parser.parse_args()


def read_json(filename):
    """Reads and parses json file"""
    with open(filename) as json_file:
        return json.load(json_file)


def get_winner(item):
    """Returns the winner of an item"""
    return item["awardedTo"].removesuffix("-WildGrowth")


def item_was_disenchanted(item):
    """Returns true if the item was disenchanted"""
    return get_winner(item) == "|de|"


def get_winning_roll(item_awarded, winner):
    """
    Returns the winning roll from a set of rolls and the player name.
    This might not be the top rolled value(eg if the item was passed)
    """
    try:
        return next(roll for roll in item_awarded["Rolls"] if roll["player"] == winner)
    except StopIteration:
        msg = "Failed to find a winner for {}".format(item_awarded["itemLink"])
        raise ValueError(msg) from None


def roll_was_bis(roll):
    """Returns true if a roll was a BiS(101) roll"""
    return roll["classification"] == "BiS"


def parse_file_for_bis_rolls(filename):
    data = read_json(filename)

    for item_awarded in data:

        # Get the winner name without the server suffix
        winner = get_winner(item_awarded)

        # Check if this was a disenchant roll -- if so, skip
        if item_was_disenchanted(item_awarded):
            continue

        # Find the winning roll
        winning_roll = get_winning_roll(item_awarded, winner)

        # Check if this was not a bis roll -- if so, skip
        if not roll_was_bis(winning_roll):
            continue

        print("{} won BiS on {}".format(winner, item_awarded["itemLink"]))


def main():
    filename = parse_args().filename
    parse_file_for_bis_rolls(filename)
