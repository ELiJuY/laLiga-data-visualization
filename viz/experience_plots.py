import numpy as np
import matplotlib.pyplot as plt

def plot_young_vs_mature_elo_imbalanced(df):
    df = df[df["elo_diff"].abs() > 10].copy()

    df["age_group"] = np.nan
    df.loc[
        (df["age_mean"] <= 26) & (df["age_diff"] <= -0.75),
        "age_group"
    ] = "Young"

    df.loc[
        (df["age_mean"] >= 26.5) & (df["age_group"].isna()),
        "age_group"
    ] = "Experienced"

    df = df.dropna(subset=["age_group"])

    df["elo_context"] = np.where(
        df["elo_diff"] > 7.5,
        "With advantage",
        "With disadvantage",
    )

    summary = (
        df
        .groupby(["elo_context", "age_group", "points"])
        .size()
        .reset_index(name="count")
    )

    summary["total"] = summary.groupby(
        ["elo_context", "age_group"]
    )["count"].transform("sum")

    summary["prop"] = summary["count"] / summary["total"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    for ax, context in zip(axes, ["With advantage", "With disadvantage"]):
        sub = summary[summary["elo_context"] == context]

        for i, pts in enumerate([0, 1, 3]):
            vals = []
            for grp in ["Young", "Experienced"]:
                v = sub[
                    (sub["age_group"] == grp) &
                    (sub["points"] == pts)
                ]["prop"]
                vals.append(v.values[0] if len(v) else 0)

            ax.bar(
                np.arange(2) + i * 0.25,
                vals,
                width=0.25,
                label=f"{pts} points" if context == "With advantage" else None
            )

        ax.set_title(context)
        ax.set_xticks(np.arange(2) + 0.25)
        ax.set_xticklabels(["Young vs Experienced", "Experienced vs Experienced"])
        ax.set_xlabel("Type of match")
        ax.grid(axis="y", alpha=0.3)

    axes[0].set_ylabel("Proportion of matches")
    axes[0].legend(title="Result")

    fig.suptitle(
        "Match outcomes in unbalanced games (|ΔELO| > 7.5)\n"
        "comparing young and experienced teams",
        fontsize=12
    )
    print(df.groupby(["elo_context", "age_group"]).size())
    plt.tight_layout()
    plt.show()


def plot_young_vs_mature_balanced(df, elo_threshold=5):
    """
    Grouped bar plot:
    Partidos igualados (|elo_diff| < elo_threshold)
    Comparación de resultados entre equipos jóvenes y maduros
    """

    df = df[df["elo_diff"].abs() < elo_threshold].copy()

    df["age_group"] = np.nan

    df.loc[
        (df["age_mean"] <= 26) & (df["age_diff"] <= -0.75),
        "age_group"
    ] = "Young vs Experienced"

    df.loc[
        (df["age_mean"] > 26.5) & (df["age_group"].isna()),
        "age_group"
    ] = "Experienced vs Experienced"

    df = df.dropna(subset=["age_group"])

    summary = (
        df
        .groupby(["age_group", "points"])
        .size()
        .reset_index(name="count")
    )

    summary["total"] = summary.groupby("age_group")["count"].transform("sum")
    summary["prop"] = summary["count"] / summary["total"]

    groups = ["Young vs Experienced", "Experienced vs Experienced"]
    points = [0, 1, 3]

    data = {
        grp: [
            summary[
                (summary["age_group"] == grp) &
                (summary["points"] == p)
            ]["prop"].values[0]
            if not summary[
                (summary["age_group"] == grp) &
                (summary["points"] == p)
            ].empty else 0
            for p in points
        ]
        for grp in groups
    }

    x = np.arange(len(groups))
    width = 0.25

    plt.figure(figsize=(8, 5))

    for i, p in enumerate(points):
        plt.bar(
            x + i * width,
            [data[g][i] for g in groups],
            width,
            label=f"{p} points"
        )

    plt.xticks(x + width, groups)
    plt.xlabel("Type of match")
    plt.ylabel("Proportion of matches")
    plt.title(
        "Match outcomes in balanced games\n"
        f"(|ΔELO| < {elo_threshold}) comparing young and experienced teams"
    )

    plt.grid(axis="y", alpha=0.3)
    plt.legend(title="Outcome")
    plt.tight_layout()
    print(df[
        (df["elo_diff"].abs() < elo_threshold)
    ].groupby("age_group").size())
    plt.show()

def table_balanced_matches_counts(df, elo_threshold=5):
    df_balanced = df[df["elo_diff"].abs() < elo_threshold].copy()

    df_balanced["age_group"] = None
    df_balanced.loc[
        (df_balanced["age_mean"] <= 26) & (df_balanced["age_diff"] <= -0.75),
        "age_group"
    ] = "Young"

    df_balanced.loc[
        (df_balanced["age_mean"] > 26.5) & (df_balanced["age_group"].isna()),
        "age_group"
    ] = "Experienced"

    df_balanced = df_balanced.dropna(subset=["age_group"])

    table = (
        df_balanced
        .groupby("age_group")
        .size()
        .reset_index(name="n_partidos")
    )

    return table

def table_imbalanced_matches_counts(df, elo_threshold=7.5):
    df_imbalanced = df[df["elo_diff"].abs() > elo_threshold].copy()

    df_imbalanced["age_group"] = None
    df_imbalanced.loc[
        (df_imbalanced["age_mean"] <= 26) & (df_imbalanced["age_diff"] <= -0.75),
        "age_group"
    ] = "Jóvenes"

    df_imbalanced.loc[
        (df_imbalanced["age_mean"] > 26.5) & (df_imbalanced["age_group"].isna()),
        "age_group"
    ] = "Maduros"

    df_imbalanced = df_imbalanced.dropna(subset=["age_group"])

    df_imbalanced["elo_context"] = np.where(
        df_imbalanced["elo_diff"] > 0,
        "Con ventaja",
        "Con desventaja"
    )

    table = (
        df_imbalanced
        .groupby(["elo_context", "age_group"])
        .size()
        .reset_index(name="n_partidos")
        .sort_values(["elo_context", "age_group"])
    )

    return table

def save_table_as_image(
    df,
    title,
    filename,
    figsize=(6, 2),
    font_size=10
):
    """
    Guarda un DataFrame como imagen usando matplotlib.
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")

    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc="center",
        cellLoc="center"
    )

    table.auto_set_font_size(False)
    table.set_fontsize(font_size)
    table.scale(1, 1.5)

    ax.set_title(title, pad=10)

    plt.tight_layout()
    plt.savefig(filename, dpi=200, bbox_inches="tight")
    plt.close()

def plot_age_mean_boxplot(df):
    """
    Boxplot de la distribución de la edad media del once inicial
    en todos los partidos.
    """

    values = df["age_mean"].dropna()

    plt.figure(figsize=(6, 5))
    plt.boxplot(values, vert=True, showfliers=True)

    plt.ylabel("Average age of the starting eleven (years)")
    plt.title("Average age distribution of the starting eleven")

    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()

    print("Statistical summary of average age:")
    print(values.describe())


def plot_elo_diff_boxplot(df):
    """
    Boxplot de la distribución de la diferencia de ELO entre equipos
    en todos los partidos.
    """
    values = df["elo_diff"].dropna()

    plt.figure(figsize=(6, 5))
    plt.boxplot(values, vert=True, showfliers=True)

    plt.ylabel("ELO difference (team - opponent)")
    plt.title("Distribution of the ELO difference between teams")

    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()

    print("Statistical summary of average ELO difference:")
    print(values.describe())

################################
# DESCARTADOS
################################

# def plot_violin_points_by_age_and_elo(df):
#     """
#     Violin plot de puntos obtenidos,
#     comparando equipos más jóvenes vs más veteranos,
#     dentro de bins de diferencia de ELO.
#     """
#
#     df_plot = df.copy()
#     df_plot = df_plot[df_plot["elo_diff"] >= 0]
#
#     def elo_bin(x):
#         x = abs(x)
#         if x <= 10:
#             return "|ΔELO| ≤ 10"
#         elif 10 < x <= 20:
#             return "10 < |ΔELO| ≤ 20"
#         else:
#             return None
#
#     df_plot["elo_bin"] = df_plot["elo_diff"].apply(elo_bin)
#     df_plot = df_plot[df_plot["elo_bin"].notna()]
#
#     def age_group(x):
#         if x <= -1.5:
#             return "Más joven"
#         elif x >= 1.5:
#             return "Más veterano"
#         else:
#             return None
#
#     df_plot["age_group"] = df_plot["age_diff"].apply(age_group)
#     df_plot = df_plot[df_plot["age_group"].notna()]
#
#     df_plot["elo_bin"] = pd.Categorical(
#         df_plot["elo_bin"],
#         categories=["|ΔELO| ≤ 10", "10 < |ΔELO| ≤ 20"],
#         ordered=True
#     )
#
#     df_plot["age_group"] = pd.Categorical(
#         df_plot["age_group"],
#         categories=["Más joven", "Más veterano"],
#         ordered=True
#     )
#
#     plt.figure(figsize=(9, 5))
#
#     sns.violinplot(
#         data=df_plot,
#         x="elo_bin",
#         y="points",
#         hue="age_group",
#         split=True,
#         inner="quartile",
#         cut=0
#     )
#
#     plt.xlabel("Diferencia de ELO entre equipos")
#     plt.ylabel("Puntos obtenidos")
#     plt.title(
#         "Distribución de puntos según edad media del once\n"
#         "controlando por diferencia de ELO"
#     )
#
#     plt.legend(title="Edad relativa del equipo")
#     plt.tight_layout()
#     plt.show()
#
# def plot_points_by_age_and_elo(df, elo_threshold=10):
#     df = df.copy()
#
#     df["age_group"] = pd.NA
#
#     df.loc[df["age_diff"] < -1.5, "age_group"] = "Más joven"
#     df.loc[df["age_diff"] > 1.5, "age_group"] = "Más veterano"
#
#     df = df.dropna(subset=["age_group"])
#
#     df["elo_group"] = np.where(
#         df["elo_diff"].abs() < elo_threshold,
#         f"|ΔELO| < {elo_threshold}",
#         f"|ΔELO| ≥ {elo_threshold}"
#     )
#
#     fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
#
#     for ax, elo_grp in zip(axes, df["elo_group"].unique()):
#         sub = df[df["elo_group"] == elo_grp]
#
#         counts = (
#             sub
#             .groupby(["age_group", "points"])
#             .size()
#             .reset_index(name="count")
#         )
#
#         totals = counts.groupby("age_group")["count"].transform("sum")
#         counts["prop"] = counts["count"] / totals
#
#         # Pivot para plot
#         pivot = counts.pivot(
#             index="age_group",
#             columns="points",
#             values="prop"
#         ).fillna(0)
#
#         x = np.arange(len(pivot.index))
#         width = 0.25
#
#         for i, pts in enumerate([0, 1, 3]):
#             if pts in pivot.columns:
#                 ax.bar(
#                     x + i * width,
#                     pivot[pts],
#                     width,
#                     label=f"{pts} puntos"
#                 )
#
#         ax.set_xticks(x + width)
#         ax.set_xticklabels(pivot.index)
#         ax.set_title(elo_grp)
#         ax.set_xlabel("Edad relativa del equipo")
#         ax.grid(axis="y", alpha=0.3)
#
#     axes[0].set_ylabel("Proporción de partidos")
#     axes[1].legend(title="Resultado")
#
#     fig.suptitle(
#         "Distribución de puntos según edad media del once\n"
#         "controlando por diferencia de ELO",
#         fontsize=13
#     )
#
#     plt.tight_layout()
#     plt.show()
