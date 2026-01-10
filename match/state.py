from football_analysis.config import *

def score_at_minute(events, minute):
    home_goals = 0
    away_goals = 0

    for e in events:
        if e["minute"] >= minute:
            continue
        if e["type"] not in GOAL_EVENTS:
            continue

        if e["team"] == "home":
            home_goals += 1
        elif e["team"] == "away":
            away_goals += 1

    return home_goals, away_goals

def players_on_field(events, minute):
    home_reds = 0
    away_reds = 0

    for e in events:
        if e["minute"] >= minute:
            continue
        if e["type"] not in RED_EVENTS:
            continue

        if e["team"] == "home":
            home_reds += 1
        elif e["team"] == "away":
            away_reds += 1

    return INITIAL_PLAYERS - home_reds, INITIAL_PLAYERS - away_reds

def match_state_at_minute(events, minute, team):
    # marcador
    home_goals, away_goals = score_at_minute(events, minute)

    # jugadores
    home_players, away_players = players_on_field(events, minute)

    if team == "home":
        diff = home_goals - away_goals
        team_players = home_players
        opp_players = away_players
    else:
        diff = away_goals - home_goals
        team_players = away_players
        opp_players = home_players

    if diff > 0:
        state = STATE_WINNING
    elif diff < 0:
        state = STATE_LOSING
    else:
        state = STATE_DRAWING

    return {
        "goal_diff": diff,
        "state": state,
        "team_players": team_players,
        "opp_players": opp_players
    }