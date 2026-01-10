from analysis.var_disallowed import *
from viz.var_plots import *
from io.loader import build_match_lookup

SEASON_FILES = [
    DATA_DIR / "season_2018-19.json",
    DATA_DIR / "season_2019-20.json",
    DATA_DIR / "season_2020-21.json",
    DATA_DIR / "season_2021-22.json",
]

if __name__ == "__main__":
    match_lookup = build_match_lookup(SEASON_FILES)

    df_var = extract_var_events(SEASON_FILES)

    df_control_candidates = build_control_candidates(SEASON_FILES, DEFAULT_BIN)
    df_control = match_controls(df_var, df_control_candidates, DEFAULT_BIN)

    df_var_analysis = build_var_analysis(df_var, match_lookup)
    df_control_analysis = build_control_analysis(df_control, match_lookup)

    df_analysis = pd.concat(
        [df_var_analysis, df_control_analysis],
        ignore_index=True
    )

    curves = build_cumulative_curves(df_analysis)

    t_var, p_var = curves[VAR_GROUP]
    t_ctrl, p_ctrl = curves[CONTROL_GROUP]

    plot_goal_curves(t_var, p_var, t_ctrl, p_ctrl)
    interaction_plot_by_state(df_analysis, horizon=15)
    boxplot_time_to_goal(df_analysis, max_t=15)
    plot_var_minute_distribution(df_var)
    plot_var_state_distribution(df_var)


    assert set(df_analysis["group"]) == {VAR_GROUP, CONTROL_GROUP}
    assert (df_analysis["t_event"] >= 0).all()
    assert (df_analysis["t_event"] <= 15).all()
    assert set(df_analysis["event_occurred"].unique()) <= {0, 1}