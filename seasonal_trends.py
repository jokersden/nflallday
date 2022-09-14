import numpy as np
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

from myutils import human_format


def get_fig_moment_season(df_daily_sales_ps, val_season):
    pivotted = (
        df_daily_sales_ps.groupby(["moment_tier", "season"])
        .agg({"avg_price": lambda x: np.log(np.mean(x))})
        .reset_index()
        .pivot("moment_tier", "season", values="avg_price")
    )

    fig_moment_season = go.Figure(
        data=go.Heatmap(
            z=pivotted.values.tolist(),
            x=pivotted.columns.tolist(),
            y=pivotted.index.tolist(),
            hoverongaps=False,
            hovertext=[human_format(item) for item in np.exp(pivotted.values).tolist()],
        )
    )
    fig_moment_season.update_traces(
        hovertemplate="<br>".join(
            ["Season: %{x}", "Tier: %{y}", "Average Price: $ %{hovertext}"]
        )
    )
    fig_moment_season.update_layout(
        title=f"Which tiers and seasons were popular {val_season}"
    )
    return fig_moment_season


def get_fig_week_season(df, val):
    df_1 = df.groupby(["season", "week"]).sum().reset_index()
    df_1 = df_1.sort_values(by="total", ascending=False)
    df_1 = pd.merge(
        df_1, df_1.groupby(["week"]).sum().reset_index(), on="week"
    ).sort_values(by="total_y", ascending=False)
    fig_week_season = px.bar(
        df_1,
        x="week",
        y="total_x",
        color="season",
        labels=dict(week="Week", total_x="Sales (USD)"),
        title=f"Which weeks produced the best moments which were bought {val}..",
    )
    return fig_week_season
