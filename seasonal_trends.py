import numpy as np

import plotly.graph_objects as go


def get_fig_moment_season(df_daily_sales_ps):
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
            hovertext=np.exp(pivotted.values).tolist(),
        )
    )
    fig_moment_season.update_traces(
        hovertemplate="<br>".join(
            ["Tier: %{x}", "Season: %{y}", "Average Price: %{hovertext:.2f} USD"]
        )
    )
    return fig_moment_season
