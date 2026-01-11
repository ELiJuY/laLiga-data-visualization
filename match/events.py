from config import *


def time_to_concede(events, minute_event, team, t_max):
    """
    Devuelve (t_event, event_occurred)
    """
    for e in sorted(events, key=lambda e: e["minute"]):
        if e["minute"] <= minute_event:
            continue
        if e["minute"] > MATCH_END_MINUTE:
            continue
        if e["type"] not in GOAL_EVENTS:
            continue

        # ¿es gol del rival?
        if e["type"] == "Own goal":
            # Own goal (home) favorece al away y viceversa
            if e["team"] == team:
                continue
        else:
            if e["team"] == team:
                continue

        t_event = e["minute"] - minute_event
        if t_event <= t_max:
            return t_event, 1

    return t_max, 0
