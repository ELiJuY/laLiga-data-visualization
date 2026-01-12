from analysis.fair_play_goleadas import build_fair_play_table
from config import DATA_DIR
from viz.fair_play_plots import (plot_yellow_rate_ratio, plot_goleada_minutes_boxplot,
                                 plot_minutes_per_yellow_goleada_vs_outside,
                                 plot_goleada_yellows_boxplot, plot_minutes_vs_yellow_ratio)

SEASON_FILES = [
    DATA_DIR / "season_2000-01.json",
    DATA_DIR / "season_2001-02.json",
    DATA_DIR / "season_2002-03.json",
    DATA_DIR / "season_2003-04.json",
    DATA_DIR / "season_2004-05.json",
    DATA_DIR / "season_2005-06.json",
    DATA_DIR / "season_2006-07.json",
    DATA_DIR / "season_2007-08.json",
    DATA_DIR / "season_2008-09.json",
    DATA_DIR / "season_2009-10.json",
    DATA_DIR / "season_2010-11.json",
    DATA_DIR / "season_2011-12.json",
    DATA_DIR / "season_2012-13.json",
    DATA_DIR / "season_2013-14.json",
    DATA_DIR / "season_2014-15.json",
    DATA_DIR / "season_2015-16.json",
    DATA_DIR / "season_2016-17.json",
    DATA_DIR / "season_2017-18.json",
    DATA_DIR / "season_2018-19.json",
    DATA_DIR / "season_2018-19.json",
    DATA_DIR / "season_2019-20.json",
    DATA_DIR / "season_2020-21.json",
    DATA_DIR / "season_2021-22.json",
]


if __name__ == "__main__":
    df_fp = build_fair_play_table(SEASON_FILES)
    # # No se va a usar
    # #plot_yellow_rate_goleadas(df_fp)
    # Gráfico principal:
    plot_yellow_rate_ratio(df_fp)
    # Gráfico secundario
    plot_minutes_per_yellow_goleada_vs_outside(df_fp)
    # # No se va a usar
    # plot_minutes_in_goleada(df_fp)
    # Gráfico de apoyo (minutos_goleada/temporada outliers)
    plot_goleada_minutes_boxplot(df_fp)
    # Gráfico de apoyo (amarillas/temporada outliers)
    plot_goleada_yellows_boxplot(df_fp)
    # # Gráfico de (rojas/minutos_goleada). No se va a usar
    # plot_red_cards_goleada_trend(df_fp)
    # Gráfico de (minutos_goleada vs ratio_amarillas)
    plot_minutes_vs_yellow_ratio(df_fp)




    # print(df_fp.head())
    # print("_________________________________________")
    # print(df_fp.tail())
    # print("_________________________________________")
    # print(df_fp.dtypes)
    # print("_________________________________________")
    # assert not df_fp.isna().any().any()
    # assert (df_fp[["minutes", "yellow", "red", "second_yellow_red"]] >= 0).all().all()
    # assert (df_fp["minutes"] > 0).all()
    #
    # minutes_per_season = (
    #     df_fp
    #     .groupby("season")["minutes"]
    #     .sum()
    # )
    #
    # print(minutes_per_season.describe())
    # print("_________________________________________")
    # print(df_fp["diff"].value_counts().sort_index())
    # print("_________________________________________")
    # check = df_fp.copy()
    # check["total_cards"] = (
    #         check["yellow"] +
    #         check["red"] +
    #         check["second_yellow_red"]
    # )
    #
    # print(check[["diff", "minutes", "total_cards"]].sort_values("diff"))
    # print("_________________________________________")
    # df_fp["yellow_rate"] = df_fp["yellow"] / df_fp["minutes"]
    # print(f"Yellow rate:\n{df_fp["yellow_rate"]}")
    # print("_________________________________________")
    # df_fp["red_rate"] = df_fp["red"] / df_fp["minutes"]
    # print(f"Red rate:\n{df_fp["red_rate"]}")
    # print("_________________________________________")
    # df_fp["second_yellow_red_rate"] = df_fp["second_yellow_red"] / df_fp["minutes"]
    # print(f"Second yellow rate:\n{df_fp["second_yellow_red_rate"]}")
    # print("_________________________________________")
    # print(
    #     df_fp[["yellow_rate", "red_rate", "second_yellow_red_rate"]]
    #     .describe()
    # )
    # print("_________________________________________")
    # print(df_fp[df_fp["season"] == "Season 2000/01"].sort_values("diff"))
    # print("_________________________________________")
    #
    #
    # df = df_fp.copy()
    #
    # df["total_reds"] = df["red"] + df["second_yellow_red"]
    #
    # reds_by_season = (
    #     df
    #     .groupby("season", as_index=False)["total_reds"]
    #     .sum()
    #     .sort_values("season")
    # )
    #
    # print(reds_by_season.describe())

