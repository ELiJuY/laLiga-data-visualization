import pandas as pd
import matplotlib.pyplot as plt
from config import GOLEADA_THRESHOLD

def plot_yellow_rate_ratio(df_fp):
    """
    Line plot del ratio:
    (amarillas/minuto en goleada) / (amarillas/minuto fuera de goleada)
    por temporada.
    """

    df_goleada = df_fp[df_fp["diff"] != "outside"].copy()
    df_outside = df_fp[df_fp["diff"] == "outside"].copy()

    goleada = (
        df_goleada
        .groupby("season", as_index=False)
        .agg({
            "yellow": "sum",
            "minutes": "sum"
        })
    )

    goleada = goleada[goleada["minutes"] > 0]
    goleada["rate_goleada"] = goleada["yellow"] / goleada["minutes"]

    outside = df_outside.copy()
    outside = outside[outside["minutes"] > 0]
    outside["rate_outside"] = outside["yellow"] / outside["minutes"]

    merged = pd.merge(
        goleada[["season", "rate_goleada"]],
        outside[["season", "rate_outside"]],
        on="season",
        how="inner"
    )

    merged["ratio"] = merged["rate_goleada"] / merged["rate_outside"]

    merged = merged.sort_values("season")

    plt.figure(figsize=(9, 5))
    plt.plot(
        merged["season"],
        merged["ratio"],
        marker="o",
        linewidth=2
    )

    plt.axhline(
        y=1.0,
        color="gray",
        linestyle="--",
        linewidth=1,
        label="Same as non-large goal-difference situation"
    )

    plt.xlabel("Season")
    plt.ylabel("Yellow card ratio (lopsided vs non-lopsided matches)")
    plt.title(
        "Relative evolution of bookings in large goal-difference situations\n"
        f"(difference ≥ {GOLEADA_THRESHOLD} goals)"
    )

    plt.xticks(rotation=45)
    plt.grid(True, axis="y", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_minutes_per_yellow_goleada_vs_outside(df_fp):
    """
    Line plot comparando los minutos por tarjeta amarilla
    en situaciones de goleada vs fuera de goleada.
    """

    df_goleada = df_fp[df_fp["diff"] != "outside"]
    df_outside = df_fp[df_fp["diff"] == "outside"]

    goleada = (
        df_goleada
        .groupby("season", as_index=False)
        .agg({
            "yellow": "sum",
            "minutes": "sum"
        })
    )

    goleada = goleada[goleada["yellow"] > 0]
    goleada["min_per_yellow_goleada"] = goleada["minutes"] / goleada["yellow"]

    outside = df_outside.copy()
    outside = outside[outside["yellow"] > 0]
    outside["min_per_yellow_outside"] = outside["minutes"] / outside["yellow"]

    merged = goleada.merge(
        outside[["season", "min_per_yellow_outside"]],
        on="season",
        how="inner"
    ).sort_values("season")

    plt.figure(figsize=(9, 5))

    plt.plot(
        merged["season"],
        merged["min_per_yellow_goleada"],
        marker="o",
        linewidth=2,
        label="Lopsided (diff ≥ 3)"
    )

    plt.plot(
        merged["season"],
        merged["min_per_yellow_outside"],
        marker="o",
        linewidth=2,
        label="Not lopsided"
    )

    plt.xlabel("Season")
    plt.ylabel("Minutes per yellow card")
    plt.title(
        "Minutes per yellow card:\n"
        f"Large goal-difference (diff ≥ {GOLEADA_THRESHOLD}) vs non-large goal-difference"
    )

    plt.xticks(rotation=45)
    plt.grid(True, axis="y", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_goleada_minutes_boxplot(df_fp):
    """
    Boxplot de los minutos totales jugados en situación de goleada
    (diff >= GOLEADA_THRESHOLD) por temporada.

    Los outliers se detectan implícitamente mediante el criterio IQR.
    """

    df_goleada = df_fp[df_fp["diff"] != "outside"]

    minutes_by_season = (
        df_goleada
        .groupby("season", as_index=False)["minutes"]
        .sum()
    )

    values = minutes_by_season["minutes"]

    plt.figure(figsize=(6, 5))
    plt.boxplot(
        values,
        vert=True,
        showfliers=True
    )

    plt.ylabel("Minutes in large goal-difference situation")
    plt.title(
        "Distribution of minutes in situations of a large goal-difference\n"
        f"(difference ≥ {GOLEADA_THRESHOLD} goals)"
    )

    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()

    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = minutes_by_season[
        (minutes_by_season["minutes"] < lower_bound) |
        (minutes_by_season["minutes"] > upper_bound)
    ]

    if not outliers.empty:
        print("Temporadas detectadas como outliers (criterio IQR):")
        print(outliers)
    else:
        print("No se detectan temporadas outlier según el criterio IQR.")

def plot_goleada_yellows_boxplot(df_fp):
    """
    Boxplot del número total de tarjetas amarillas
    en situaciones de goleada (diff >= GOLEADA_THRESHOLD) por temporada.

    Los outliers se detectan implícitamente mediante el criterio IQR.
    """

    df_goleada = df_fp[df_fp["diff"] != "outside"]

    yellows_by_season = (
        df_goleada
        .groupby("season", as_index=False)["yellow"]
        .sum()
    )

    values = yellows_by_season["yellow"]

    plt.figure(figsize=(6, 5))
    plt.boxplot(
        values,
        vert=True,
        showfliers=True
    )

    plt.ylabel("Yellow cards in large goal-difference situation")
    plt.title(
        "Distribution of yellow cards in situations of a large goal-difference\n"
        f"(difference ≥ {GOLEADA_THRESHOLD} goals)"
    )

    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()

    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = yellows_by_season[
        (yellows_by_season["yellow"] < lower_bound) |
        (yellows_by_season["yellow"] > upper_bound)
    ]

    if not outliers.empty:
        print("Temporadas detectadas como outliers (criterio IQR):")
        print(outliers)
    else:
        print("No se detectan temporadas outlier según el criterio IQR.")



def plot_minutes_vs_yellow_ratio(df_fp):
    """
    Scatter plot:
    - Eje X: minutos totales en situación de goleada por temporada
    - Eje Y: ratio de amarillas (goleada / no goleada)
    """

    df_goleada = df_fp[df_fp["diff"] != "outside"]

    goleada = (
        df_goleada
        .groupby("season", as_index=False)
        .agg({
            "minutes": "sum",
            "yellow": "sum"
        })
    )
    goleada = goleada[goleada["minutes"] > 0]
    goleada["rate_goleada"] = goleada["yellow"] / goleada["minutes"]

    df_outside = df_fp[df_fp["diff"] == "outside"].copy()
    df_outside = df_outside[df_outside["minutes"] > 0]
    df_outside["rate_outside"] = df_outside["yellow"] / df_outside["minutes"]

    merged = goleada.merge(
        df_outside[["season", "rate_outside"]],
        on="season",
        how="inner"
    )

    merged["ratio"] = merged["rate_goleada"] / merged["rate_outside"]

    plt.figure(figsize=(7, 5))
    plt.scatter(
        merged["minutes"],
        merged["ratio"],
        alpha=0.7
    )

    plt.axhline(
        y=1.0,
        color="gray",
        linestyle="--",
        linewidth=1,
        label="Same as non-large goal-difference situation"
    )

    plt.xlabel("Minutes in large goal-difference situation (per season)")
    plt.ylabel("Yellow card ratio (large goal-difference / non large goal-difference)")
    plt.title(
        "Relationship between minutes of scoring\n"
        "and relative severity of bookings"
    )

    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

################################
# DESCARTADOS
################################
#
# RED_BLOCK_SIZE = 3
#
# def plot_red_cards_goleada_trend(df_fp):
#     """
#     Gráfico exploratorio de la tendencia de tarjetas rojas
#     en situaciones de goleada (diff >= GOLEADA_THRESHOLD),
#     agrupando temporadas en bloques de tamaño RED_BLOCK_SIZE.
#     """
#
#     # Filtrar solo situaciones de goleada
#     df_goleada = df_fp[df_fp["diff"] != "outside"]
#
#     # Agregar por temporada
#     reds_by_season = (
#         df_goleada
#         .groupby("season", as_index=False)
#         .agg({
#             "red": "sum",
#             "second_yellow_red": "sum"
#         })
#     )
#
#     # Total de expulsiones
#     reds_by_season["total_reds"] = (
#         reds_by_season["red"] + reds_by_season["second_yellow_red"]
#     )
#
#     # Orden temporal
#     reds_by_season = reds_by_season.sort_values("season").reset_index(drop=True)
#
#     # Crear bloques
#     reds_by_season["block"] = (
#         reds_by_season.index // RED_BLOCK_SIZE
#     )
#
#     grouped = (
#         reds_by_season
#         .groupby("block")
#         .agg({
#             "season": ["first", "last"],
#             "total_reds": "mean"
#         })
#         .reset_index(drop=True)
#     )
#
#     grouped.columns = ["season_start", "season_end", "mean_reds"]
#
#     # Etiquetas del eje X
#     grouped["season_label"] = (
#         grouped["season_start"] + "–" + grouped["season_end"]
#     )
#
#     # Plot
#     plt.figure(figsize=(8, 5))
#     plt.plot(
#         grouped["season_label"],
#         grouped["mean_reds"],
#         marker="o",
#         linewidth=2
#     )
#
#     plt.xlabel("Bloque de temporadas")
#     plt.ylabel("Media de tarjetas rojas en goleadas")
#     plt.title(
#         "Tendencia exploratoria de tarjetas rojas en situaciones de goleada\n"
#         f"(agrupadas cada {RED_BLOCK_SIZE} temporadas)"
#     )
#
#     plt.xticks(rotation=45)
#     plt.grid(True, axis="y", alpha=0.3)
#     plt.tight_layout()
#     plt.show()
#
# def plot_yellow_rate_goleadas(df_fp):
#
#     df_goleada = df_fp[df_fp["diff"] != "outside"].copy()
#
#     grouped = (
#         df_goleada
#         .groupby("season", as_index=False)
#         .agg({
#             "yellow": "sum",
#             "minutes": "sum"
#         })
#     )
#
#     grouped["yellow_rate"] = grouped["yellow"] / grouped["minutes"]
#
#     grouped = grouped.sort_values("season")
#
#     plt.figure(figsize=(9, 5))
#     plt.plot(
#         grouped["season"],
#         grouped["yellow_rate"],
#         marker="o",
#         linewidth=2
#     )
#
#     plt.xlabel("Temporada")
#     plt.ylabel("Tarjetas amarillas por minuto (goleada)")
#     plt.title(
#         "Evolución de las tarjetas amarillas en situaciones de goleada\n"
#         f"(diferencia ≥ {GOLEADA_THRESHOLD} goles)"
#     )
#
#     plt.grid(True, axis="y", alpha=0.3)
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.show()
#
#     def plot_minutes_in_goleada(df_fp):
#         """
#         Line plot de los minutos totales jugados en situación de goleada
#         (diff >= GOLEADA_THRESHOLD) por temporada.
#         """
#
#         df_goleada = df_fp[df_fp["diff"] != "outside"]
#
#         minutes = (
#             df_goleada
#             .groupby("season", as_index=False)["minutes"]
#             .sum()
#             .sort_values("season")
#         )
#
#         plt.figure(figsize=(9, 5))
#         plt.plot(
#             minutes["season"],
#             minutes["minutes"],
#             marker="o",
#             linewidth=2
#         )
#
#         plt.xlabel("Season")
#         plt.ylabel("Large goal-difference situation minutes")
#         plt.title(
#             f"Total minutes played in large goal-difference situations\n"
#             f"(difference ≥ {GOLEADA_THRESHOLD} goals)"
#         )
#
#         plt.xticks(rotation=45)
#         plt.grid(True, axis="y", alpha=0.3)
#         plt.tight_layout()
#         plt.show()