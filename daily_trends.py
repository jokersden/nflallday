import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

pio.templates.default = "plotly_dark"


def get_daily_trends(df_sum):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(x=df_sum["date"], y=df_sum["total"], name="Daily Sales Volume(USD)"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=df_sum.date, y=df_sum.sales, name="Number of Daily Sales"),
        secondary_y=True,
    )
    fig.add_vrect(
        x0="2022-08-04",
        x1="2022-08-07",
        annotation_text="Hall of Fame Weekend",
        annotation_position="inside top right",
        annotation_textangle=90,
        annotation_font_size=16,
        annotation_font_color="orange",
        fillcolor="yellow",
        line_color="white",
        opacity=0.25,
        line_width=2,
        line_dash="solid",
    )

    fig.add_vline(
        x="2022-08-04",
        line_color="white",
        line_width=2,
        line_dash="dash",
    )
    fig.add_annotation(
        x="2022-08-04",
        y=395000,
        text=f"Preseason start",
        yanchor="top",
        showarrow=True,
        arrowhead=1,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        font=dict(size=16, color="green", family="Courier New, monospace, bold"),
        bordercolor="green",
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.6,
    )

    fig.add_vrect(
        x0="2022-08-11",
        x1="2022-08-14",
        annotation_text="First Preseason Weekend",
        annotation_position="inside top left",
        annotation_textangle=90,
        annotation_font_size=16,
        annotation_font_color="gray",
        fillcolor="Green",
        opacity=0.3,
        line_width=0,
        line_dash="dash",
    )

    fig.add_vrect(
        x0="2022-08-18",
        x1="2022-08-22",
        annotation_text="Second Preseason Weekend",
        annotation_position="inside top left",
        annotation_textangle=90,
        annotation_font_size=16,
        annotation_font_color="gray",
        fillcolor="Green",
        opacity=0.3,
        line_color="white",
        line_width=0,
        line_dash="dash",
    )

    fig.add_vrect(
        x0="2022-08-25",
        x1="2022-08-28",
        annotation_text="Third Preseason Weekend",
        annotation_position="inside top left",
        annotation_textangle=90,
        annotation_font_size=16,
        annotation_font_color="gray",
        fillcolor="Green",
        opacity=0.3,
        line_width=0,
    )

    fig.add_vline(
        x="2022-08-28",
        line_color="white",
        line_width=2,
        line_dash="dash",
    )
    fig.add_annotation(
        x="2022-08-28",
        y=395000,
        text=f"Preseason end",
        yanchor="top",
        showarrow=True,
        arrowhead=1,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        font=dict(size=16, color="green", family="Courier New, monospace, bold"),
        bordercolor="green",
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.6,
    )
    fig.update_xaxes(title="Date")
    fig.update_yaxes(title="Number of Sales", secondary_y=True)
    fig.update_yaxes(title="Sales Volume (USD)", secondary_y=False)
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig


def get_daily_team_fig(df_daily_sales):
    df_team = df_daily_sales.groupby(["team", "date"]).sum().reset_index()
    df_team = pd.merge(df_team, df_team.groupby("date").sum().reset_index(), on="date")
    df_team["perc"] = df_team.total_x * 100 / df_team.total_y
    fig_team_perc = px.area(
        df_team,
        x="date",
        y="perc",
        color="team",
        labels=dict(perc="Percentage (%)", date="Date"),
    )

    fig_team_perc.add_vrect(
        x0="2022-08-04",
        x1="2022-08-07",
        annotation_text="Hall of Fame Weekend",
        annotation_position="inside top left",  # annotation_textangle = 90,
        annotation_font_size=14,
        annotation_font_color="white",
        # fillcolor="yellow",
        line_color="white",
        opacity=1,
        line_width=2,
        line_dash="dash",
    )

    fig_team_perc.add_vrect(
        x0="2022-08-11",
        x1="2022-08-14",
        annotation_text="First Preseason Weekend",
        annotation_position="inside top left",  # annotation_textangle = 90,
        annotation_font_size=14,
        annotation_font_color="white",
        # fillcolor="Green",
        opacity=1,
        line_width=2,
        line_dash="dash",
    )

    fig_team_perc.add_vrect(
        x0="2022-08-18",
        x1="2022-08-22",
        annotation_text="Second Preseason Weekend",
        annotation_position="inside top left",  # annotation_textangle = 90,
        annotation_font_size=14,
        annotation_font_color="white",
        # fillcolor="Green",
        opacity=1,
        line_color="white",
        line_width=2,
        line_dash="dash",
    )

    fig_team_perc.add_vrect(
        x0="2022-08-25",
        x1="2022-08-28",
        annotation_text="Third Preseason Weekend",
        annotation_position="inside top left",  # annotation_textangle = 90,
        annotation_font_size=14,
        annotation_font_color="white",
        # fillcolor="Green",
        opacity=1,
        line_width=2,
        line_dash="dash",
    )

    return fig_team_perc
