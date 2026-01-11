import pandas as pd
from datetime import datetime

from config import HOME_TEAM, AWAY_TEAM, DATA_DIR
from data_io.loader import load_season


def compute_age(dob, match_date):
    if match_date.tzinfo is not None:
        match_date = match_date.replace(tzinfo=None)

    return (match_date - dob).days / 365.25


def build_age_elo_dataframe(season_files):
    rows = []

    for season_file in season_files:
        season_data = load_season(season_file)

        players = {
            p["href"]: p
            for p in season_data["players"]
        }

        for rnd in season_data["rounds"]:
            for match in rnd["matches"]:

                match_date = datetime.fromisoformat(
                    match["date_time"].replace("Z", "")
                )

                home_goals, away_goals = match["result"]

                if home_goals > away_goals:
                    home_pts, away_pts = 3, 0
                elif home_goals < away_goals:
                    home_pts, away_pts = 0, 3
                else:
                    home_pts, away_pts = 1, 1

                for team, lineup, pts in [
                    (HOME_TEAM, match["home_lineup"], home_pts),
                    (AWAY_TEAM, match["away_lineup"], away_pts),
                ]:
                    ages = []
                    elos = []

                    for player_href in lineup:
                        if player_href not in players:
                            continue

                        p = players[player_href]

                        if not p.get("dob") or p.get("elo") is None:
                            continue

                        dob = datetime.fromisoformat(p["dob"])
                        age = compute_age(dob, match_date)

                        ages.append(age)
                        elos.append(p["elo"])

                    if len(ages) < 7 or len(elos) < 7:
                        continue

                    rows.append({
                        "season": season_data["season_id"],
                        "team": team,
                        "points": pts,
                        "age_mean": sum(ages) / len(ages),
                        "elo_mean": sum(elos) / len(elos),
                        "match_id": match["id"]
                    })

    df = pd.DataFrame(rows)

    df = df.merge(
        df,
        on="match_id",
        suffixes=("", "_opp")
    )

    df = df[df["team"] != df["team_opp"]]

    df["age_diff"] = df["age_mean"] - df["age_mean_opp"]
    df["elo_diff"] = df["elo_mean"] - df["elo_mean_opp"]

    df = df[[
        "season",
        "team",
        "points",
        "age_mean",
        "elo_mean",
        "age_diff",
        "elo_diff"
    ]]

    return df



