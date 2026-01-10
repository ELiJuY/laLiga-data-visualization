import numpy as np
from matplotlib import pyplot as plt

from config import *


def plot_goal_curves(t_var, p_var, t_ctrl, p_ctrl):

    plt.figure(figsize=(8, 5))
    plt.plot(t_var, p_var, label="VAR anulado", linewidth=2)
    plt.plot(t_ctrl, p_ctrl, label="Control (sin evento)", linewidth=2)

    plt.xlabel("Minutos desde el evento")
    plt.ylabel("Probabilidad acumulada de encajar gol")
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

    plt.xlabel("Grupo")
    plt.ylabel(f"P(encajar gol ≤ {horizon} min)")
    plt.title("Interaction plot: efecto VAR según estado del partido")
    plt.legend(title="Estado")
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
    plt.boxplot(data, labels=["VAR anulado", "Control"], showfliers=True)
    plt.ylabel("Minutos hasta encajar gol")
    plt.title("Distribución del tiempo hasta encajar gol")
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.show()

def plot_var_minute_distribution(df_var, bin_width=5):

    bins = np.arange(0, 100, bin_width)

    plt.figure(figsize=(8, 4))
    plt.hist(df_var["minute"], bins=bins, edgecolor="black")

    plt.xlabel("Minuto del partido")
    plt.ylabel("Número de goles anulados por VAR")
    plt.title("Distribución temporal de los goles anulados por VAR")
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

    plt.xlabel("Estado del equipo al anularse el gol")
    plt.ylabel("Número de eventos")
    plt.title("Estado del marcador en goles anulados por VAR")
    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.show()
