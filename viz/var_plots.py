import numpy as np
from matplotlib import pyplot as plt

from config import *


def plot_goal_curves(t_var, p_var, t_ctrl, p_ctrl):

    plt.figure(figsize=(8, 5))
    plt.plot(t_var, p_var, label="VAR disallowed", linewidth=2)
    plt.plot(t_ctrl, p_ctrl, label="Control (no event)", linewidth=2)

    plt.xlabel("Minutes after the event")
    plt.ylabel("Cumulative probability of conceding a goal")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def interaction_plot_by_state(df_analysis, horizon=15):
    states = ["winning", "drawing", "losing"]
    groups = ["VAR", "CONTROL"]

    means = {state: [] for state in states}

    for state in states:
        for group in groups:
            df_sub = df_analysis[
                (df_analysis["state"] == state) &
                (df_analysis["group"] == group)
            ]
            prob = (
                (df_sub["event_occurred"] & (df_sub["t_event"] <= horizon)).mean()
                if len(df_sub) > 0 else np.nan
            )
            means[state].append(prob)

    plt.figure(figsize=(8, 5))
    for i, state in enumerate(states):
        plt.plot(groups, means[state], marker="o", label=state)

    plt.xlabel("Group")
    plt.ylabel(f"P(conceding goal ≤ {horizon} min)")
    plt.title("VAR effect depending on the state of the match")
    plt.legend(title="State")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def boxplot_time_to_goal(df_analysis, max_t=15):
    df_goals = df_analysis[
        (df_analysis["event_occurred"] == 1) &
        (df_analysis["t_event"] <= max_t)
    ]

    data = [
        df_goals[df_goals["group"] == "VAR"]["t_event"],
        df_goals[df_goals["group"] == "CONTROL"]["t_event"]
    ]

    plt.figure(figsize=(6, 5))
    plt.boxplot(data, labels=["VAR disallowed", "Control"], showfliers=True)
    plt.ylabel("Minutes until goal conceded")
    plt.title("Time distribution until conceding a goal")
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.show()

def plot_var_minute_distribution(df_var, bin_width=5):

    bins = np.arange(0, 100, bin_width)

    plt.figure(figsize=(8, 4))
    plt.hist(df_var["minute"], bins=bins, edgecolor="black")

    plt.xlabel("Minute of the match")
    plt.ylabel("Number of goals disallowed by VAR")
    plt.title("Temporal distribution of goals disallowed by VAR")
    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.show()

def plot_var_state_distribution(df_var):
    import matplotlib.pyplot as plt

    counts = df_var["state"].value_counts().reindex(
        [STATE_WINNING, STATE_DRAWING, STATE_LOSING]
    )

    plt.figure(figsize=(6, 4))
    plt.bar(counts.index, counts.values)

    plt.xlabel("Team state when the goal was disallowed")
    plt.ylabel("Number of events")
    plt.title("Scoreboard status for goals disallowed by VAR")
    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.show()
