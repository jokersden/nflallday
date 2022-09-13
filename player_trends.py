import numpy as np
import pandas as pd

import plotly.express as px


def get_fig_player_seasons(df_daily_sales_ps_player_season, val_player):
    df_daily_sales_ps_player_season.loc[
        df_daily_sales_ps_player_season.player == "N/A", "player"
    ] = "Team Play"

    df_daily_sales_ps_player_season = (
        df_daily_sales_ps_player_season.groupby(["player", "season"])
        .agg({"total": lambda x: (np.sum(x))})
        .reset_index()
    )
    df_daily_sales_ps_player_season = pd.merge(
        df_daily_sales_ps_player_season,
        df_daily_sales_ps_player_season.groupby(["player"])
        .sum()
        .reset_index()
        .nlargest(50, columns="total"),
        on="player",
    ).sort_values(by="total_y", ascending=False)

    return px.bar(
        df_daily_sales_ps_player_season,
        x="player",
        y="total_x",
        color="season",
        category_orders={"player": df_daily_sales_ps_player_season["player"].to_list()},
        title=f"Top 50 most valuable players {val_player}",
        labels=dict(total_x="Value (USD)", player="Player Name"),
    )


def get_fig_moment_playtype(df, val_player):
    df_daily_sales_moment_playtype = (
        df.groupby(["play_type", "moment_tier"]).sum().reset_index()
    )
    fig_moment_playtype = px.bar(
        df_daily_sales_moment_playtype,
        x="play_type",
        y="total",
        color="moment_tier",
        text="total",
        title=f"What moments were most sought out {val_player}",
        labels=dict(play_type="Play Type", total="Amount (USD)", moment_tier="Tier"),
    )
    fig_moment_playtype.update_traces(
        hovertemplate="<br>".join(
            [
                "Play Type: %{x}",
                "Volume: $%{y:,.2f}",
            ]
        )
    )
    fig_moment_playtype.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig_moment_playtype