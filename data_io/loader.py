import json

def load_season(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def build_match_lookup(season_files):
    lookup = {}

    for season_file in season_files:
        season_data = load_season(season_file)

        for rnd in season_data["rounds"]:
            for match in rnd["matches"]:
                lookup[match["id"]] = match

    return lookup