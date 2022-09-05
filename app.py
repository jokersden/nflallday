import os
from datetime import datetime
import pandas as pd
import streamlit as st

from shroomdk import ShroomDK

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

pio.templates.default = "plotly_dark"

API_KEY = os.getenv("API_KEY")
sdk = ShroomDK(API_KEY)

st.set_page_config(
    page_title="NFL All Day - Preseason",
    page_icon=":football:",
    layout="wide",
    menu_items=dict(About="it's a work of joker#2418"),
)
st.title(":football: NFL All Day - Preseason! :football:")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
# st.markdown(hide_st_style, unsafe_allow_html=True)
st.success("Please Note: All the dates and time are in US/New York time.", icon="⏰")


@st.cache(allow_output_mutation=True, ttl=30 * 60)
def load_data():
    daily_sales_sql = f"""
    select 
        convert_timezone('UTC', 'America/New_York', block_timestamp::timestamp_ntz)::date as date, 
        moment_tier, 
        player, 
        team, 
        season, 
        avg(price) as avg_price, 
        sum(price) as total, 
        count(distinct seller) as sellers,
        count(distinct buyer) as buyers, 
        count(distinct tx_id) as sales 
    from flow.core.ez_nft_sales s
        inner join flow.core.dim_allday_metadata m 
            on m.nft_collection=s.nft_collection 
            and m.nft_id=s.nft_id
    where 
        block_timestamp >= '2022-08-01' 
        and TX_SUCCEEDED='TRUE'
    group by date, moment_tier, player, team, season
    """
    return pd.DataFrame(sdk.query(daily_sales_sql).records)


st.text("")
date_col1, date_col2 = st.columns(2)
date_col1.metric(
    "Preseason start date",
    "4th of August",
)
date_col2.metric(
    "Preseason end date",
    "28th of August",
)
st.header("")
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "All Days - Daily trends",
        "Teams trends",
        "Player trends",
        "Seasonal trends",
        "About",
    ]
)

df_daily_sales = load_data()
df_daily_sales.date = pd.to_datetime(df_daily_sales.date)
df_sum = df_daily_sales.groupby("date").sum().reset_index()
df_preseason = df_sum[df_sum.date >= datetime(2022, 8, 4)]
df_preseason = df_preseason[df_preseason.date <= datetime(2022, 8, 28)]

with tab1:
    st.subheader("How did daily sales go during this Preseason")

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
    # fig.update_layout(title="How did daily Sales volume change?")

    st.plotly_chart(fig, use_container_width=True)
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Total Sales Volume in Preseason(USD)", df_preseason.total.sum())
    m_col2.metric("Total number of Sales in Preseason", df_preseason.sales.sum())
    m_col3.metric(
        "Day with the highest sales volume in the Preseason",
        str(
            df_preseason[
                df_preseason.total == df_preseason.total.max()
            ].date.dt.date.values[0]
        ),
    )

    weekends = df_preseason[
        df_preseason.date.isin(
            [
                datetime(2022, 8, 4),
                datetime(2022, 8, 5),
                datetime(2022, 8, 6),
                datetime(2022, 8, 7),
                datetime(2022, 8, 11),
                datetime(2022, 8, 12),
                datetime(2022, 8, 13),
                datetime(2022, 8, 14),
                datetime(2022, 8, 18),
                datetime(2022, 8, 19),
                datetime(2022, 8, 20),
                datetime(2022, 8, 21),
                datetime(2022, 8, 22),
                datetime(2022, 8, 25),
                datetime(2022, 8, 26),
                datetime(2022, 8, 27),
                datetime(2022, 8, 28),
            ]
        )
    ]

    non_weekends = df_preseason[
        ~df_preseason.date.isin(
            [
                datetime(2022, 8, 4),
                datetime(2022, 8, 5),
                datetime(2022, 8, 6),
                datetime(2022, 8, 7),
                datetime(2022, 8, 11),
                datetime(2022, 8, 12),
                datetime(2022, 8, 13),
                datetime(2022, 8, 14),
                datetime(2022, 8, 18),
                datetime(2022, 8, 19),
                datetime(2022, 8, 20),
                datetime(2022, 8, 21),
                datetime(2022, 8, 22),
                datetime(2022, 8, 25),
                datetime(2022, 8, 26),
                datetime(2022, 8, 27),
                datetime(2022, 8, 28),
            ]
        )
    ]

    m_col4.metric(
        "The Volumes in Weekends than in other days",
        f"{round(weekends.total.sum() / non_weekends.total.sum(), 1)}X",
    )
    st.info(
        "The interest seems to have picked up with the Preseason, specially in the **Hall of Fame Weekend** and The **Second Preseason Weekend**. On average weekends saw a **3.6 X** increase in sales volume than the other days during the preseason. However the interest had died down since the Third weekend."
    )

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
    st.markdown("""---""")
    st.text("")
    st.subheader("Do the match schedule impact the team popularity")
    st.plotly_chart(fig_team_perc, use_container_width=True)
    g_col1, g_col2 = st.columns(2)
    g_col1.image(
        "https://raw.githubusercontent.com/jokersden/nflallday/main/images/hof.png"
    )
    g_col2.image(
        "https://raw.githubusercontent.com/jokersden/nflallday/main/images/w1_rav.png"
    )
    st.info(
        "The Hall of Fame weekend and first Weekend, Jaguars and Ravens certainly had some fans,"
        " During the Hall of Fame Weekend when Jaguars played against Raiders, Jaguars seemed to have an uptick in the sales volume accounting for 15.7% of the total sales volume on 5th of August and 12.4% of the total sales volume on 6th of August"
        " even though they were beaten in that game. \n"
        "On the other hand the victorious Ravens had become a fan favorite during the 1st weekend of the preseason with 20.8% of the total sales volume on the game day, 12th and 10+% of all the sales during the next two days."
        "Green Bay Packers were also pretty hot in the second preseason weekend which shows that the game schedules have a big correlation with fans buying/selling their moments."
    )

    st.error("Team trends in next tab...", icon="🏈")

with tab2:
    pass
with tab5:
    st.write(
        "This was created by joker#2418 as a part of the tournament organized by FlipsideCrypto on NFL AllDay data. Following source was used to find dates and other info: https://operations.nfl.com/gameday/nfl-schedule/2022-23-important-nfl-dates/"
    )
    st.write(
        "Since the NFTs live on Flow chain, ```flow.core.ez_nft_sales``` along with ```flow.core.dim_allday_metadata``` tables were used. The dates were converted to US/New York time as the blockchain data is in UTC and the game is predominantly played, watched in the US, the times may not tell the story correctly if we don't adjust the times. Below is the SQL code:"
    )
    st.code(
        """select 
        convert_timezone('UTC', 'America/New_York', block_timestamp::timestamp_ntz)::date as date, 
        moment_tier, 
        player, 
        team, 
        season, 
        avg(price) as avg_price, 
        sum(price) as total, 
        count(distinct seller) as sellers,
        count(distinct buyer) as buyers, 
        count(distinct tx_id) as sales 
    from flow.core.ez_nft_sales s
        inner join flow.core.dim_allday_metadata m 
            on m.nft_collection=s.nft_collection 
            and m.nft_id=s.nft_id
    where 
        block_timestamp >= '2022-08-01' 
        and TX_SUCCEEDED='TRUE'
    group by date, moment_tier, player, team, season""",
        language="sql",
    )
