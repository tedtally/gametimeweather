import json
from dotenv import load_dotenv
import requests
import os
import arrow as ar
import rapidapi_sports_feed as rsf
import cfbd as cfb
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
from tqdm import tqdm

def main():
    # Page setting
    st.set_page_config(layout="wide", page_title="Tally's Betting Dashboard :clipboard:")

    st.session_state.update(st.session_state)
    #--- Init session_state
    if 'active_page' not in st.session_state:
        st.session_state.active_page = 'gamestream'

    load_dotenv()

    st.write("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fascinate');

        /* Move block container higher */
        div.block-container.css-jr6cdq e1tzin5v0 {
            margin-top: -9em;
        }

        /* Adjustments for the logo image*/

        img {
            display: block;
            /*margin-top: 1.5em;*/
        }

        /* Centering text in each gray box */
        div.css-1ht1j8u.e16fv1kl0 {
            text-align: center;
        }

        /* Third line of Row */
        div.css-wnm74r.e16fv1kl3 {
            margin-left: 30%;
            margin-right: 20%;
        }

        /* Row 1 */
        div.css-1r6slb0.e1tzin5v2 {
            background-color: rgb(63, 79, 107);
            padding: 3% 3% 3% 3%;
            border-radius: 5px;
        }

        /* Row 2 */
        div.css-12w0qpk.e1tzin5v2 {
            background-color: rgba(220, 220, 220, 0.60);
            padding: 3% 3% 3% 3%;
            border-radius: 5px;
        }
        div.css-dm3ece.everg990{

        }

        /* Hide hamburger menu and footer */
        div.css-14xtw13.e8zbici0{
            display: none;
        }

        footer.css-ipbk5a.egzxvld4 {
            display: none;
        }

        footer.css-12gp8ed.eknhn3m4 {
            display: none;
        }

        div.vg-tooltip-element {
            display: none;
        }
        div.css-fblp2m{
            display: none;
        }
        footer {

            visibility: hidden;

        }
            div.dvn-scroller {
                background-color: #f5f5f5;
                width: 100%;    
            }

        div.css-434r0z{
                background-color: #f5f5f5;
                width: 100%;
            }
        div.css-1ftupb1 e1tzin5v2{
                background-color: #333333;
                width: 100%;
            }
        </style>
        """, unsafe_allow_html=True)
    
    startdate = ar.utcnow().to('local').format('YYYY-MM-DD')
    cfb_weekdays = [3,4,5]
    weekday = 5
    weeks = list(range(1,15+1))

    def get_game_date(start, dayofweek):
        """
        @startdate: given date, in format '2013-05-25'
        @weekday: week day as a integer, between 0 (Monday) to 6 (Sunday)
        """        
        d = datetime.strptime(start, '%Y-%m-%d')
        t = timedelta((7 + dayofweek - d.weekday()) % 7)
        #print((d + t).strftime('%Y-%m-%d'))
        return (d + t).strftime('%Y-%m-%d')


    df_list = []
    #cols = []
    #for x in cfb_weekdays:
    #    df_temp = rsf.get_games(get_game_date(startdate, x))
    #    if len(df_temp) > 0:
    #        for x in df_temp:
    #            df_list.append(x)

    tqdm_segm_labels = tqdm(df_list)
    df_list = cfb.get_games(startdate)

    df = pd.DataFrame(data=df_list)
    st.cache(df)

    def handle_interval():
        if st.session_state.my_interval:
            st.session_state.my_interval = week_interval

    col1, col2, col3, col4 = st.columns([4,4,4, 4], gap="medium")
    #with col1:
    st.session_state.my_interval = "All"
    # filter by date, week, year, team, conference
    with col1:
        weekdays = st.multiselect('Show CFB Game Days', cfb_weekdays)
    with col2:
        test =  st.multiselect('Select a locations', [1,2,3])
    with col3:
        week_interval = st.radio('Select week', (weeks), on_change=handle_interval, horizontal=True)    
    with col4:
        d = st.date_input("As Of Date")

    new_df = df

    if weekdays:
        st.write(weekdays[0])
        gdate = get_game_date(startdate, weekdays[0]) #get_game_date(startdate, weekdays[0])
        st.write(gdate)
        new_df = new_df[new_df['game_date'].isin([gdate])]

    if week_interval:
        st.write(week_interval)
        df = pd.DataFrame(data=cfb.get_games(startdate, week_interval))
        st.cache(df)
        new_df = df
        #new_df = new_df[new_df['week']==intervals]

    if d:
        st.write(d)
        new_df = new_df[new_df['game_date']<=d.strftime('%Y-%m-%d')]
        
    st._legacy_dataframe(new_df)

# get game info from rapidapi_sports_feed
# use rapidapi's venue or city and state to get weather info from accuweather
# use cfbd to get betting lines, records, stats using user input of year, week, division

if __name__ == "__main__":
    main()