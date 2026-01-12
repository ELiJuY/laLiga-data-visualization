import pandas as pd
from collections import defaultdict

from config import MATCH_START_MINUTE, MATCH_END_MINUTE, GOLEADA_THRESHOLD, CARD_EVENTS
from match.state import score_at_minute
from data_io.loader import load_season


def goleada_intervals(events):
    """
    Devuelve una lista de intervalos [start, end] (ambos inclusive)
    en los que algún equipo va perdiendo por GOLEADA_THRESHOLD o más goles.
    """
    intervals = []

    in_goleada = False
    start_minute = None

    for minute in range(MATCH_START_MINUTE, MATCH_END_MINUTE + 1):
        home_goals, away_goals = score_at_minute(events, minute)
        diff = home_goals - away_goals

        goleada_now = abs(diff) >= GOLEADA_THRESHOLD

        # Empieza la goleada
        if goleada_now and not in_goleada:
            start_minute = min(minute + 1, MATCH_END_MINUTE)
            in_goleada = True
        # Termina la goleada
        elif not goleada_now and in_goleada:
            if start_minute <= minute - 1:
                intervals.append({
                    "start": start_minute,
                    "end": minute - 1
                })
            in_goleada = False
            start_minute = None

    # Si el partido termina en goleada
    if in_goleada and start_minute and start_minute <= MATCH_END_MINUTE:
        intervals.append({
            "start": start_minute,
            "end": MATCH_END_MINUTE
        })

    return intervals

def accumulate_minutes_by_diff(events, accumulator):
    """
    Acumula minutos jugados en situación de goleada,
    desglosados por diferencia exacta de goles.

    accumulator: dict[int, int]
        clave = diferencia de goles (3, 4, 5, ...)
        valor = minutos acumulados
    """
    intervals = goleada_intervals(events)

    for interval in intervals:
        for minute in range(interval["start"], interval["end"] + 1):
            home_goals, away_goals = score_at_minute(events, minute)
            diff = abs(home_goals - away_goals)

            if diff < GOLEADA_THRESHOLD:
                continue

            accumulator[diff] = accumulator.get(diff, 0) + 1

def minute_in_goleada(minute, intervals):
    for interval in intervals:
        if interval["start"] <= minute <= interval["end"]:
            return True
        # permitir descuento
        if minute > MATCH_END_MINUTE and interval["end"] == MATCH_END_MINUTE:
            return True
    return False

def accumulate_cards_by_diff(events, accumulator):
    """
    Acumula tarjetas producidas durante situaciones de goleada,
    desglosadas por diferencia exacta de goles.

    accumulator: dict[str, dict[int, int]]
        {
          "Yellow card": {3: x, 4: y, ...},
          "Red card": {...},
          "2nd yellow card leads to red card": {...}
        }
    """
    intervals = goleada_intervals(events)

    if not intervals:
        return

    for e in events:
        event_type = e["type"]
        minute = e["minute"]

        if event_type not in CARD_EVENTS:
            continue

        if not minute_in_goleada(minute, intervals):
            continue

        home_goals, away_goals = score_at_minute(events, minute)
        diff = abs(home_goals - away_goals)

        if diff < GOLEADA_THRESHOLD:
            continue

        if event_type not in accumulator:
            accumulator[event_type] = {}

        accumulator[event_type][diff] = accumulator[event_type].get(diff, 0) + 1

def accumulate_minutes_outside_goleada(events, accumulator):
    """
    Acumula minutos jugados fuera de situación de goleada (diff < GOLEADA_THRESHOLD).
    """
    intervals = goleada_intervals(events)

    for minute in range(MATCH_START_MINUTE, MATCH_END_MINUTE + 1):
        if minute_in_goleada(minute, intervals):
            continue

        home_goals, away_goals = score_at_minute(events, minute)
        diff = abs(home_goals - away_goals)

        if diff < GOLEADA_THRESHOLD:
            accumulator["minutes"] += 1

def accumulate_cards_outside_goleada(events, accumulator):
    """
    Acumula tarjetas producidas fuera de situaciones de goleada.
    """
    intervals = goleada_intervals(events)

    for e in events:
        event_type = e["type"]
        minute = e["minute"]

        if event_type not in CARD_EVENTS:
            continue

        if minute_in_goleada(minute, intervals):
            continue

        home_goals, away_goals = score_at_minute(events, minute)
        diff = abs(home_goals - away_goals)

        if diff < GOLEADA_THRESHOLD:
            accumulator[event_type] += 1

def build_fair_play_table(season_files):
    """
    Construye una tabla con métricas de fair play en situaciones de goleada
    y fuera de goleada.

    Devuelve un DataFrame con columnas:
    - season
    - diff (int para goleada, "outside" para no goleada)
    - minutes
    - yellow
    - red
    - second_yellow_red
    """
    rows = []

    for season_file in season_files:
        season_data = load_season(season_file)
        season_id = season_data["season_id"]

        minutes_by_diff = defaultdict(int)

        cards_by_diff = {
            "Yellow card": defaultdict(int),
            "Red card": defaultdict(int),
            "2nd yellow card leads to red card": defaultdict(int)
        }

        minutes_outside = {"minutes": 0}

        cards_outside = {
            "Yellow card": 0,
            "Red card": 0,
            "2nd yellow card leads to red card": 0
        }

        for rnd in season_data["rounds"]:
            for match in rnd["matches"]:
                events = match["events"]

                # goleada
                accumulate_minutes_by_diff(events, minutes_by_diff)
                accumulate_cards_by_diff(events, cards_by_diff)

                # fuera de goleada
                accumulate_minutes_outside_goleada(events, minutes_outside)
                accumulate_cards_outside_goleada(events, cards_outside)

        diffs = sorted(
            d for d in minutes_by_diff.keys()
            if d >= GOLEADA_THRESHOLD
        )

        for diff in diffs:
            rows.append({
                "season": season_id,
                "diff": diff,
                "minutes": minutes_by_diff.get(diff, 0),
                "yellow": cards_by_diff["Yellow card"].get(diff, 0),
                "red": cards_by_diff["Red card"].get(diff, 0),
                "second_yellow_red": cards_by_diff["2nd yellow card leads to red card"].get(diff, 0)
            })

        rows.append({
            "season": season_id,
            "diff": "outside",
            "minutes": minutes_outside["minutes"],
            "yellow": cards_outside["Yellow card"],
            "red": cards_outside["Red card"],
            "second_yellow_red": cards_outside["2nd yellow card leads to red card"]
        })

    return pd.DataFrame(rows)
