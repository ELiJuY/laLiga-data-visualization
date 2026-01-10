from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

HOME_TEAM = "home"
AWAY_TEAM = "away"

INITIAL_PLAYERS = 11

MATCH_START_MINUTE = 1
MATCH_END_MINUTE = 90
MATCH_MAX_MINUTE_ITER = 97

DEFAULT_BIN = 2
DEFAULT_N_CONTROLS = 5

MIN_ANALYSIS_MINUTE = 15
MAX_ANALYSIS_WINDOW = 15

CONTROL_RANDOM_SEED = 42

VAR_GROUP = "VAR"
CONTROL_GROUP = "CONTROL"

STATE_WINNING = "winning"
STATE_DRAWING = "drawing"
STATE_LOSING = "losing"

GOAL_EVENTS = {
    "Goal",
    "Goal from penalty",
    "Own goal"
}

RED_EVENTS = {
    "Red card",
    "2nd yellow card leads to red card"
}

VAR_EVENT_TYPE = "Goal disallowed by VAR"