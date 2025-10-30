import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime

st.set_page_config(page_title="Global Insights Dashboard", page_icon="🌍", layout="wide")

st.title("🌍 Global Insights Dashboard: COVID-19 & Economic Trends")
st.markdown("Analyze **COVID-19 cases** and **economic indicators (GDP, Unemployment)** in real-time across countries using live APIs.")

@st.cache_data(show_spinner=False)
def get_covid_data():
    url = "https://disease.sh/v3/covid-19/historical/all?lastdays=365"
    res = requests.get(url)
    data = res.json()
    df = pd.DataFrame({
        "Date": list(data["cases"].keys()),
        "Confirmed": list(data["cases"].values()),
        "Deaths": list(data["deaths"].values()),
        "Recovered": list(data["recovered"].values())
    })
    df["Date"] = pd.to_datetime(df["Date"])
    return df

@st.cache_data(show_spinner=False)
def get_economic_data(country_code="IN"):
    indicators = {"GDP": "NY.GDP.MKTP.CD", "Unemployment": "SL.UEM.TOTL.ZS"}
    econ_data = {}
    for key, indicator in indicators.items():
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json&per_page=100"
        resp = requests.get(url).json()
        if len(resp) > 1:
            econ_data[key] = pd.DataFrame(resp[1])[["date", "value"]].rename(columns={"date": "Year", "value": key})
    merged = pd.merge(econ_data["GDP"], econ_data["Unemployment"], on="Year", how="outer")
    merged = merged.dropna().sort_values("Year")
    merged["Year"] = merged["Year"].astype(int)
    merged["Country"] = country_code
    return merged

with st.sidebar:
    st.header("⚙️ Dashboard Controls")
    country_code = st.text_input("Enter Country ISO Code (e.g., IN, US, CN):", "IN").upper()
    refresh = st.button("🔄 Refresh Data")

covid_df = get_covid_data()
econ_df = get_economic_data(country_code)
st.caption(f"📅 Data last updated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

col1, col2 = st.columns(2)
with col1:
    st.subheader("🦠 COVID-19 Global Trend (Last 12 Months)")
    covid_fig = px.line(covid_df, x="Date", y=["Confirmed", "Recovered", "Deaths"],
                        title="COVID-19 Global Trend", markers=True, template="plotly_white")
    st.plotly_chart(covid_fig, use_container_width=True)

with col2:
    st.subheader(f"💹 Economic Indicators — {country_code}")
    econ_fig = px.line(econ_df, x="Year", y=["GDP", "Unemployment"],
                       title=f"GDP & Unemployment Trends ({country_code})", markers=True, template="plotly_white")
    st.plotly_chart(econ_fig, use_container_width=True)

st.subheader("📊 GDP vs COVID Impact")
merged = econ_df.copy()
merged["Confirmed"] = covid_df["Confirmed"].iloc[-len(merged):].values
corr_fig = px.scatter(merged, x="GDP", y="Confirmed", size="Unemployment", color="Year",
                      title=f"GDP vs COVID Confirmed Cases ({country_code})", template="plotly_white")
st.plotly_chart(corr_fig, use_container_width=True)

st.success("✅ Dashboard ready! Data fetched live from World Bank & disease.sh APIs.")

st.markdown("---")
st.markdown("**Created by [Mahi Jindal](https://www.linkedin.com/in/mahi-jindal)** | GitHub: [18mahi](https://github.com/18mahi)")
