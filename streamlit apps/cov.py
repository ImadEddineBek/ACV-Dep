import pandas as pd
import altair as alt
import streamlit as st
import urllib
import warnings
import numpy as np

warnings.filterwarnings('ignore')


def main():
    def make_new(data):
        if new_daily:
            return data - np.concatenate([pd.DataFrame([[0] * len(data.columns)], columns=data.columns), data[:-1]])
        return data

    @st.cache
    def get_un_data():
        source = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_"
        DATA = source + 'confirmed_global.csv'
        DATA1 = source + 'deaths_global.csv'
        DATA2 = source + 'recovered_global.csv'
        df = pd.read_csv(DATA)
        dfcountries = df.drop(['Lat', 'Long'], axis=1).groupby('Country/Region').sum().transpose()

        dfcountries.index = pd.to_datetime(dfcountries.index)
        df1 = pd.read_csv(DATA1)
        dfcountries1 = df1.drop(['Lat', 'Long'], axis=1).groupby('Country/Region').sum().transpose()

        dfcountries1.index = pd.to_datetime(dfcountries1.index)
        df2 = pd.read_csv(DATA2)
        dfcountries2 = df2.drop(['Lat', 'Long'], axis=1).groupby('Country/Region').sum().transpose()

        dfcountries2.index = pd.to_datetime(dfcountries2.index)
        return dfcountries, dfcountries1, dfcountries2

    try:
        cases, deaths, recoveries = get_un_data()
    except urllib.error.URLError as e:
        st.error(
            """
            **This demo requires internet access.**

            Connection error: %s
        """
            % e.reason
        )
        return e
    max_norm = st.sidebar.checkbox('Normalize all countries to the same max length.')
    new_daily = st.sidebar.checkbox('New daily values instead of accumulating values.')
    countries = st.sidebar.multiselect(
        "Choose countries", list(cases.columns), ["China", "US"]
    )
    if not countries:
        st.error("Please select at least one country.")
        return
    data = make_new(cases[countries])
    # print(data)
    if max_norm:
        data /= data.max(axis=0)
    data = data.T
    st.write("### Covid Cases:", data.sort_index())
    data = data.T.reset_index()
    data = pd.melt(data, id_vars=["index"]).rename(
        columns={"index": "day", "value": "Covid Cases"})
    chart = (
        alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
            x="day:T",
            y=alt.Y("Covid Cases:Q", stack=None),
            color="Country/Region:N",
        )
    )
    st.altair_chart(chart, use_container_width=True)

    data = make_new(deaths[countries])
    if max_norm:
        data /= data.max(axis=0)
    data = data.T
    st.write("### Covid Deaths:", data.sort_index())
    data = data.T.reset_index()
    data = pd.melt(data, id_vars=["index"]).rename(
        columns={"index": "day", "value": "Covid Deaths"})
    chart = (
        alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
            x="day:T",
            y=alt.Y("Covid Deaths:Q", stack=None),
            color="Country/Region:N",
        )
    )
    st.altair_chart(chart, use_container_width=True)

    data = make_new(recoveries[countries])
    if max_norm:
        data /= data.max(axis=0)
    data = data.T
    st.write("### Covid Recoveries:", data.sort_index())
    data = data.T.reset_index()
    data = pd.melt(data, id_vars=["index"]).rename(
        columns={"index": "day", "value": "Covid Recoveries"})
    chart = (
        alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
            x="day:T",
            y=alt.Y("Covid Recoveries:Q", stack=None),
            color="Country/Region:N",
        )
    )
    st.altair_chart(chart, use_container_width=True)


if __name__ == '__main__':
    main()
