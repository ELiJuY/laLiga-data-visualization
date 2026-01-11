from analysis.age_experience import build_age_elo_dataframe
from config import DATA_DIR
from viz.experience_plots import (plot_young_vs_mature_elo_imbalanced, plot_young_vs_mature_balanced,
                                  table_balanced_matches_counts, save_table_as_image,
                                  table_imbalanced_matches_counts, plot_elo_diff_boxplot, plot_age_mean_boxplot)

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
    df = build_age_elo_dataframe(SEASON_FILES)
    # # No se ve bien la diferencia
    # plot_violin_points_by_age_and_elo(df)
    # # Esta mal definido
    # plot_points_by_age_and_elo(df)
    plot_young_vs_mature_elo_imbalanced(df)
    plot_young_vs_mature_balanced(df)
    plot_elo_diff_boxplot(df)
    plot_age_mean_boxplot(df)

    table_balanced = table_balanced_matches_counts(df)

    save_table_as_image(
        table_balanced,
        title="Volumen de partidos igualados por tipo de equipo",
        filename="tabla_partidos_igualados.png",
        figsize=(5, 2.5)
    )

    table_imbalanced = table_imbalanced_matches_counts(df)

    save_table_as_image(
        table_imbalanced,
        title="Volumen de partidos desequilibrados por contexto y tipo de equipo",
        filename="tabla_partidos_desequilibrados.png",
        figsize=(6, 3)
    )
    # print(df.head())
    # print("_________________________________")
    # print(df.describe())
    # print("_________________________________")
    # print(df["elo_diff"].value_counts(bins=6))
    # print("_________________________________")
    # print(df["age_diff"].abs().describe())
