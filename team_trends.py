import numpy as np
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

from myutils import human_format


def get_fig_team_season(df_daily_sales_ps, val_team):
    pivotted = (
        df_daily_sales_ps.groupby(["season", "team"])
        .agg({"avg_price": lambda x: np.log(np.mean(x))})
        .reset_index()
        .pivot("season", "team", values="avg_price")
    )

    fig_team_season_avg = go.Figure(
        data=go.Heatmap(
            z=pivotted.values.tolist(),
            x=pivotted.columns.tolist(),
            y=pivotted.index.tolist(),
            hoverongaps=False,
            hovertext=np.exp(pivotted.values).tolist(),
        ),
    )
    fig_team_season_avg.update_traces(
        hovertemplate="<br>".join(
            ["Team: %{x}", "Season: %{y}", "Average Price: $ %{hovertext:.2f}"]
        )
    )
    # st.subheader("Which team had priceless moments")
    fig_team_season_avg.update_layout(
        title=f"Which moments were most priceless {val_team} (Average price per NFT)",
        yaxis={
            "title": "Season",
        },
        xaxis={"title": "Team", "tickangle": 45},
        # yaxis_nticks=len(pivotted.index)
    )
    return fig_team_season_avg


def get_fig_moment(df_daily_sales_ps, val_team):
    df_daily_sales_ps_moment = (
        df_daily_sales_ps.groupby(["team", "moment_tier"])
        .sum()
        .reset_index()
        .sort_values(by="total", ascending=False)
    )
    df_daily_sales_ps_moment = pd.merge(
        df_daily_sales_ps_moment,
        df_daily_sales_ps_moment.groupby(["team"]).sum().reset_index(),
        # .nlargest(50, columns="total"),
        on="team",
    ).sort_values(by="total_y", ascending=False)

    fig_moment = px.bar(
        df_daily_sales_ps_moment,
        x="team",
        y="total_x",
        color="moment_tier",
        text="total_x",
        labels=dict(team="Team", moment_tier="Tier", total_x="Volume (USD)"),
        category_orders={"team": df_daily_sales_ps_moment["team"].to_list()},
    )
    fig_moment.update_layout(title=f"Teams sales based on moment tier {val_team}")
    fig_moment.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig_moment


def get_fig_team_season_total(df_daily_sales_ps, val_team):
    pivotted = (
        df_daily_sales_ps.groupby(["team", "season"])
        .agg({"total": lambda x: np.log(np.sum(x))})
        .reset_index()
        .pivot("season", "team", values="total")
    )

    fig_team_season_tot = go.Figure(
        data=go.Heatmap(
            z=pivotted.values.tolist(),
            x=pivotted.columns.tolist(),
            y=pivotted.index.tolist(),
            hoverongaps=False,
            hovertext=[human_format(item) for item in np.exp(pivotted.values).tolist()],
        )
    )

    fig_team_season_tot.update_traces(
        hovertemplate="<br>".join(
            ["Team: %{x}", "Season: %{y}", "Total Volume: $ %{hovertext}"]
        )
    )
    fig_team_season_tot.update_layout(
        title=f"Which teams and seasons amongst the highest total value {val_team} (Total $$ value)",
        yaxis={
            "title": "Season",
        },
        xaxis={"title": "Team", "tickangle": 45},
        # yaxis_nticks=len(pivotted.index)
    )
    return fig_team_season_tot
