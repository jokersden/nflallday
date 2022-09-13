import os
from datetime import datetime
import pandas as pd
import numpy as np
import streamlit as st

from shroomdk import ShroomDK

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

from daily_trends import get_daily_team_fig, get_daily_trends
from player_trends import (
    get_fig_moment_player_position,
    get_fig_moment_playtype,
    get_fig_player_seasons,
    get_fig_player_seasons_price,
)
from seasonal_trends import get_fig_moment_season
from team_trends import get_fig_moment, get_fig_team_season, get_fig_team_season_total
from utils import get_non_weekends, get_weekends, human_format

pio.templates.default = "plotly_dark"

API_KEY = os.getenv("API_KEY")
sdk = ShroomDK(API_KEY)

st.set_page_config(
    page_title="NFL All Day - Preseason",
    page_icon=":football:",
    layout="wide",
    menu_items=dict(About="it's a work of joker#2418"),
)
# st.markdown(
#    """
# <iframe
#    frameborder="0"
#    height="100%"
#    width="100%"
#    src="https://youtube.com/embed/VjDsksvzXwg?autoplay=1&controls=0&showinfo=0&autohide=1&loop=1"
#  >
#  </iframe>
#    """,
#    unsafe_allow_html=True,
# )

st.image(
    "https://wwwimage-us.pplusstatic.com/base/files/blog/nflquizheaderimage.jpeg",
    use_column_width=True,
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


@st.cache(allow_output_mutation=True, ttl=30 * 60, show_spinner=False)
def load_data():
    daily_sales_sql = f"""
    select 
        convert_timezone('UTC', 'America/New_York', block_timestamp::timestamp_ntz)::date as date, 
        moment_tier, 
        player, 
        team, 
        season, 
        play_type,
        MOMENT_STATS_FULL:metadata:playerPosition as player_position,
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
    group by date, moment_tier, player, team, season, play_type, player_position
    """
    return pd.DataFrame(sdk.query(daily_sales_sql).records)


st.text("")
date_col1, date_col2, date_col3 = st.columns(3)
date_col1.metric(
    "Preseason start date",
    "4th of August",
)
date_col2.metric("", "")
date_col3.metric(
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

with st.spinner("Stay tight lads, we're throwing around the old pig skin..."):
    df_daily_sales = load_data()
df_daily_sales.date = pd.to_datetime(df_daily_sales.date)
df_sum = df_daily_sales.groupby("date").sum().reset_index()
df_preseason = df_sum[df_sum.date >= datetime(2022, 8, 4)]
df_preseason = df_preseason[df_preseason.date <= datetime(2022, 8, 28)]
df_since_preseason = df_daily_sales[df_daily_sales.date > datetime(2022, 8, 28)]
df_daily_sales_ps = df_daily_sales[df_daily_sales.date >= datetime(2022, 8, 4)]
df_daily_sales_ps = df_daily_sales_ps[df_daily_sales_ps.date <= datetime(2022, 8, 28)]

dataframes = {
    "After Preseason": df_since_preseason,
    "During Preseason": df_daily_sales_ps,
}

with tab1:
    st.subheader("How did daily sales go during this Preseason")
    st.plotly_chart(get_daily_trends(df_sum), use_container_width=True)

    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric(
        "Total Sales Volume in Preseason(USD)", f"$ {df_preseason.total.sum()}"
    )
    m_col2.metric("Total number of Sales in Preseason", df_preseason.sales.sum())
    m_col3.metric(
        "Day with the highest sales volume in the Preseason",
        str(
            df_preseason[
                df_preseason.total == df_preseason.total.max()
            ].date.dt.date.values[0]
        ),
    )

    m_col4.metric(
        "The Volumes in Weekends than in other days in Preseason",
        f"{round(get_weekends(df_preseason).total.sum() / get_non_weekends(df_preseason).total.sum(), 1)}X",
    )
    st.info(
        "The interest seems to have picked up with the Preseason, specially in the **Hall of Fame Weekend** and The **Second Preseason Weekend**. On average weekends saw a **3.6 X** increase in sales volume than the other days during the preseason. However the interest had died down since then but the fan interest has picked up since the start of the season."
    )

    st.markdown("""---""")
    st.text("")
    st.subheader("Do the match schedule impact the team popularity")
    st.plotly_chart(get_daily_team_fig(df_daily_sales), use_container_width=True)
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
    gcol3, gcol4 = st.columns(2)
    gcol4.image(
        "https://raw.githubusercontent.com/jokersden/nflallday/main/images/bills.png"
    )
    gcol3.info(
        "The interest seems to have skyrocketted with the start of new season. The Bills have 25% of the sales on both "
        "8th and 9th with the victory of the opening match. Rams seems to have had some interest among fans before their game "
        "with Bills on 7th and 8th September."
    )

    st.error("Team trends in next tab...", icon="🏈")

with tab2:
    st.error(
        "You can switch between preseason data and data since preseason from below."
    )
    val_team = st.selectbox(
        "Select the timeframe",
        options=["During Preseason", "After Preseason"],
        key="team",
    )

    st.plotly_chart(
        get_fig_moment(dataframes[val_team], val_team), use_container_width=True
    )
    st.warning(
        "ULTIMATE tier has been added after the Preseason... New York Giants were the first to sell the first Ultimate tier moment!!"
    )
    st.info(
        "During the Preseason Jacksonwille Jaguars were very popular and they have sold the highest volume in sales, followed by the Packers."
        " However, 49ers was Legendary because they were the highest in terms of legendary tier volume and Raiders had all their sales in Legendary tier but volume wasn't big compared to other teams."
        "After the preseason and the first weekend of the season, Bills have turned around the tables and already (on 13th of September) accounted for the"
        " highest amount of sales volume. Their victory against Rams on 9th may have sparked some interest among the fans to buy some of their exclusive moments."
    )
    team_col1, team_col2 = st.columns(2)
    team_col1.plotly_chart(
        get_fig_team_season_total(dataframes[val_team], val_team),
        use_container_width=True,
    )

    team_col2.plotly_chart(
        get_fig_team_season(dataframes[val_team], val_team), use_container_width=True
    )
    st.info(
        "Moments from 2021 were obviously the fan favorite in terms of the total value and also majority of the teams "
        "had sold 2021 moments more often than other years. Packers seems to have priceless moments across multiple years/seasons"
        " than any other team? Does this mean they are pretty consistent and a fan favorite throughout the time?"
        " Vikings 2009 moments were the most priceless suring the preseason as it had the highest average price among all the teams across seasons."
        ""
        "Interestingly, New York Giants have sold the most priceless moments after the preseason end till now (13th Sept), the Giants were able to sell the Ultimate tier."
        " Even post preseason time period shows the legendary Packers have their moments being sold across multiple seasons than many other team. Again I am asking YOU, are packers consistently produce important moments in literally every season? :) "
        " Although Bills have the highest volume that predominantly coming from 2021 season's moments."
    )
    st.error("Player trends in next tab...", icon="🏈")


with tab3:
    st.error(
        "You can switch between preseason data and data since preseason from below."
    )
    val_player = st.selectbox(
        "Select the timeframe",
        options=["During Preseason", "After Preseason"],
        key="player",
    )

    st.plotly_chart(
        get_fig_player_seasons(dataframes[val_player], val_player),
        use_container_width=True,
    )
    st.info(
        "Well well well, Tom Brady and his 2021 moments have been what fans have spent their $$ on, barring the N/A or Team Play as a player. "
        "41 out of top 50 most sold players during preseason, found that successful moments in 2021. "
        " However since the preseason ended on 28th August, Gabriel Davis has taken the spotlight so far (13th of September). Interestingly Julio Jones who is at 4th amongst the most sold player since preseason ends, "
        "and his 2011 moments were also sold apart from the 2021 moments. Similar trends can be seen for Stefon Diggs, Davante Adams"
        " Odell Beckham Jr and Richard Sherman. Where their previous seasons have also surfaced along with 2021 moments."
    )

    st.plotly_chart(
        get_fig_player_seasons_price(dataframes[val_player], val_player),
        use_container_width=True,
    )
    st.info(
        "QB (quaterback) position seems to be the fan favorite, where they'd pay a high price to get moments from players who plays that position like Trey Lance, Aaron Rodgers"
        " Trevor Lawrance, Tom Brady to name a few. And the other player position that people wanted at a higher price was WR (Wide Receiver)."
        " during both preseason and after preseason Trey Lance, who plays QB, had his moments which were significantly higher than the other players."
    )
    st.plotly_chart(
        get_fig_moment_playtype(dataframes[val_player], val_player),
        use_container_width=True,
    )
    st.info(
        "Although Player Melt produced higher amount with legendary tier moments, Reception gained most $$ from moments sales during preseason as well as after preseason, followed by Pass during the preseason but Rush overtook Pass after preseason sales (insight: 13th Sept)."
        " Ineterestingly Reception had the first Ultimate tier moment as well."
    )
    st.plotly_chart(
        get_fig_moment_player_position(dataframes[val_player], val_player),
        use_container_width=True,
    )
    st.info(
        "Although 2-Pt Attempt with a particular player position were pricier during the preseason sales, Tight End Player melts became more dominant in terms of the average price "
        "since the end of the preseason until 13th Sept (at the time of this writing). However it was not that TE Player melt suddenly became pricier but the other moments with play types and positions which were pricier"
        " previously during preseason, weren't seen on sale since the end of preseason, for example DL Pressure was $2.8K on average during preseason but Pressure play type wasn't on sale since 28th August to today, 13th September."
    )

with tab4:
    st.error(
        "You can switch between preseason data and data since preseason from below."
    )
    val_season = st.selectbox(
        "Select the timeframe",
        options=["During Preseason", "After Preseason"],
        key="season",
    )
    st.plotly_chart(
        get_fig_moment_season(dataframes[val_season], val_season),
        use_container_width=True,
    )
    st.info(
        "Of course Legendary tier is expensive, and the legendary tier 2021 moments were the most expensive. However, After preseason an Ultimate tier 2014 moments were sold which is pricier than legendary."
    )


with tab5:
    st.write(
        "Hey friends, This was created by joker#2418 as a part of the tournament organized by FlipsideCrypto on NFL AllDay data. This dashboard was intended to show different trends in the buying during the Preseason specifically and then after the preseason. The insights were added on 13th of Spetember although the dashboard updates with ShroomDK. Following source was used to find dates and other info: https://operations.nfl.com/gameday/nfl-schedule/2022-23-important-nfl-dates/"
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
        play_type,
        MOMENT_STATS_FULL:metadata:playerPosition as player_position,
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
    group by date, moment_tier, player, team, season, play_type, player_position""",
        language="sql",
    )
