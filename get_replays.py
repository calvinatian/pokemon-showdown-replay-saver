"""
https://replay.pokemonshowdown.com/search.json?format=gen9ou
"""

import requests
import argparse
from pathlib import Path

VALID_FORMATS = [
    "gen9randombattle",
    "gen9ou",
    "gen9ubers",
    "gen9uu",
    "gen9ru",
    "gen9nu",
    "gen9pu",
    "gen9lc",
    "gen9monotype",
    "gen9battlestadiumsingles",
    "gen9cap",
    "gen9randomdoublesbattle",
    "gen9doublesou",
    "gen9vgc2023",
    "gen9balancedhackmons",
    "gen9mixandmega",
    "gen9almostanyability",
    "gen9stabmons",
    "gen9nfe",
    "gen9godlygift",
    "gen8randombattle",
    "gen8ou",
    "gen7randombattle",
    "gen7ou",
    "gen6randombattle",
    "gen6ou",
    "gen5randombattle",
    "gen5ou",
    "gen4ou",
    "gen3ou",
    "gen2ou",
    "gen1ou",
]


def get_replays(format):
    """Get replays from Pokemon Showdown for a given format"""
    url = f"https://replay.pokemonshowdown.com/search.json?format={format}"
    response = requests.get(url)
    data = response.json()
    return data


def save_replay(id, format, log_format="inputlog", output_dir="logs"):
    """Save a replay from Pokemon Showdown"""
    # https://replay.pokemonshowdown.com/gen8randombattle-2005209836.inputlog
    url = f"https://replay.pokemonshowdown.com/{id}.{log_format}"
    response = requests.get(url)
    
    if response.status_code != 200 or response.text == "":
        return False

    Path(f"{output_dir}/{format}").mkdir(parents=True, exist_ok=True)
    with open(f"{output_dir}/{format}/{id}.{log_format}", "w") as f:
        f.write(response.text)
    return True


def main():
    # Set up arguments
    parser = argparse.ArgumentParser(description="Get replays from Pokemon Showdown")
    parser.formatter_class = lambda prog: argparse.ArgumentDefaultsHelpFormatter(prog, max_help_position=32)
    parser.add_argument(
        "format",
        help=f"The format of the battles to get. Valid formats: {', '.join(VALID_FORMATS)}",
        choices=VALID_FORMATS,
        default="gen9ou",
        metavar="",
    )
    parser.add_argument(
        "--limit",
        help="The number of replays to get (default 10 most recent)",
        default=10,
        type=int,
    )
    parser.add_argument(
        "--output",
        help="The format of the output: inputlog may not be supported for certain formats",
        default="json",
        choices=["json", "inputlog", "log"],
    )
    parser.add_argument(
        "--output_dir",
        help="The directory to save the logs to",
        default="logs",
    )
    args = parser.parse_args()

    # Save replays
    data = get_replays(args.format)

    for replay in data[: args.limit]:
        id = replay["id"]
        if save_replay(id, args.format, args.output, args.output_dir):
            print(f"Saved replay {id}.{args.output}")
        else:
            print(f"Failed to save replay {id}.{args.output}")

if __name__ == "__main__":
    main()
