import numpy as np
import pandas as pd

from config import *
from io.loader import load_season
from match.events import time_to_concede
from match.state import players_on_field, score_at_minute, match_state_at_minute

RELEVANT_EVENTS = {
    "Goal",
    "Goal from penalty",
    "Own goal",
    "Goal disallowed",
    "Goal disallowed by VAR",
    "Red card",
    "2nd yellow card leads to red card",
    "Missed penalty",
    "Penalty saved"
}

def extract_var_events(season_files):
    VAR_EVENTS = []

    season_file: str
    for season_file in season_files:
        season_data = load_season(season_file)

        for rnd in season_data["rounds"]:
            for match in rnd["matches"]:
                events = match["events"]

                for e in events:
                    if e["type"] != VAR_EVENT_TYPE:
                        continue

                    minute = e["minute"]
                    team = e["team"]

                    # Numero de jugadores de cada equipo
                    home_players, away_players = players_on_field(events, minute)

                    if team == "home":
                        team_players = home_players
                        opp_players = away_players
                    else:
                        team_players = away_players
                        opp_players = home_players

                    # Marcador, diferencia de goles del partido, estado del partido
                    home_goals, away_goals = score_at_minute(events, minute)

                    if team == "home":
                        goal_diff = home_goals - away_goals
                    else:
                        goal_diff = away_goals - home_goals

                    if goal_diff > 0:
                        state = STATE_WINNING
                    elif goal_diff < 0:
                        state = STATE_LOSING
                    else:
                        state = STATE_DRAWING

                    VAR_EVENTS.append({
                        "season": season_data["season_id"],
                        "match_id": match["id"],
                        "minute": minute,
                        "team": team,
                        "home_goals": home_goals,
                        "away_goals": away_goals,
                        "goal_diff": goal_diff,
                        "state": state,
                        "team_players": team_players,
                        "opp_players": opp_players
                    })
    return pd.DataFrame(VAR_EVENTS)

def build_control_candidates(season_files, BIN):
    CONTROL_CANDIDATES = []

    for season_file in season_files:
        season_data = load_season(season_file)

        for rnd in season_data["rounds"]:
            for match in rnd["matches"]:
                events = match["events"]

                # indexar eventos por minuto
                events_by_minute = {}
                for e in events:
                    events_by_minute.setdefault(e["minute"], []).append(e)

                for minute in range(MATCH_START_MINUTE, MATCH_MAX_MINUTE_ITER):
                    # excluir si hay evento relevante en el minute-bin
                    skip = False
                    for m in range(minute - BIN, minute + 1):
                        for e in events_by_minute.get(m, []):
                            if e["type"] in RELEVANT_EVENTS:
                                skip = True
                                break
                        if skip:
                            break
                    if skip:
                        continue

                    for team in ["home", "away"]:
                        state_info = match_state_at_minute(events, minute, team)

                        CONTROL_CANDIDATES.append({
                            "season": season_data["season_id"],
                            "match_id": match["id"],
                            "minute": minute,
                            "team": team,
                            "state": state_info["state"],
                            "goal_diff": state_info["goal_diff"],
                            "team_players": state_info["team_players"],
                            "opp_players": state_info["opp_players"]
                        })

    return pd.DataFrame(CONTROL_CANDIDATES)

def match_controls(df_var, df_control_candidates, BIN, n_controls=DEFAULT_N_CONTROLS):
    CONTROL_SAMPLES = []

    for _, var_row in df_var.iterrows():
        candidates = df_control_candidates[
            (df_control_candidates["state"] == var_row["state"]) &
            (df_control_candidates["team"] == var_row["team"]) &
            (df_control_candidates["team_players"] == INITIAL_PLAYERS) &
            (df_control_candidates["opp_players"] == INITIAL_PLAYERS) &
            (abs(df_control_candidates["minute"] - var_row["minute"]) <= BIN)
        ]

        if len(candidates) == 0:
            continue

        sampled = candidates.sample(
            n=min(n_controls, len(candidates)),
            replace=False,
            random_state=CONTROL_RANDOM_SEED
        )

        for _, row in sampled.iterrows():
            CONTROL_SAMPLES.append({
                **row.to_dict(),
                "var_minute": var_row["minute"]
            })

    return pd.DataFrame(CONTROL_SAMPLES)


def build_var_analysis(df_var, match_lookup, min_minute=MIN_ANALYSIS_MINUTE):
    analysis_rows = []

    for _, row in df_var.iterrows():
        minute = row["minute"]
        if minute < min_minute:
            continue

        t_max = min(MAX_ANALYSIS_WINDOW, MATCH_END_MINUTE - minute)
        if t_max <= 0:
            continue

        match = match_lookup[row["match_id"]]
        events = match["events"]

        t_event, occurred = time_to_concede(
            events,
            minute,
            row["team"],
            t_max
        )

        analysis_rows.append({
            "group": VAR_GROUP,
            "state": row["state"],
            "t_event": t_event,
            "event_occurred": occurred
        })

    return pd.DataFrame(analysis_rows)

def build_control_analysis(df_control, match_lookup, min_minute=MIN_ANALYSIS_MINUTE):
    analysis_rows = []

    for _, row in df_control.iterrows():
        minute = row["minute"]
        var_minute = row["var_minute"]

        if var_minute < min_minute:
            continue

        t_max = min(MAX_ANALYSIS_WINDOW, MATCH_END_MINUTE - var_minute)
        if t_max <= 0:
            continue

        match = match_lookup[row["match_id"]]
        events = match["events"]

        t_event, occurred = time_to_concede(
            events,
            minute,
            row["team"],
            t_max
        )

        analysis_rows.append({
            "group": CONTROL_GROUP,
            "state": row["state"],
            "t_event": t_event,
            "event_occurred": occurred
        })

    return pd.DataFrame(analysis_rows)

def cumulative_goal_curve(df, max_t):
    times = np.arange(0, max_t + 1)
    cumulative_prob = []

    N = len(df)

    for t in times:
        events_occurred = df[
            (df["event_occurred"] == 1) &
            (df["t_event"] <= t)
        ]

        cumulative_prob.append(len(events_occurred) / N)

    return times, cumulative_prob

def build_cumulative_curves(df_analysis, max_t=MAX_ANALYSIS_WINDOW):
    curves = {}

    for group in [VAR_GROUP, CONTROL_GROUP]:
        df_group = df_analysis[df_analysis["group"] == group]
        times, probs = cumulative_goal_curve(df_group, max_t)
        curves[group] = (times, probs)

    return curves

