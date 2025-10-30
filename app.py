{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "669cec56-f305-492a-99a4-b182dc5b8020",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import plotly.express as px\n",
    "import requests\n",
    "import datetime"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "9cd7f2f9-0464-45dd-b567-003c60f7e5bd",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-10-30 16:10:20.752 WARNING streamlit.runtime.scriptrunner_utils.script_run_context: Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:10:20.752 WARNING streamlit.runtime.scriptrunner_utils.script_run_context: Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:10:21.995 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run C:\\Users\\jinda\\AppData\\Roaming\\Python\\Python311\\site-packages\\ipykernel_launcher.py [ARGUMENTS]\n",
      "2025-10-30 16:10:21.995 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:10:21.995 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:10:21.999 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "st.set_page_config(\n",
    "    page_title=\"Global Insights Dashboard\",\n",
    "    page_icon=\"🌍\",\n",
    "    layout=\"wide\"\n",
    ")\n",
    "\n",
    "st.title(\"🌍 Global Insights Dashboard: COVID-19 & Economic Trends\")\n",
    "st.markdown(\"Analyze **COVID-19 cases** and **economic indicators (GDP, Unemployment)** in real-time across countries using live APIs.\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "f9cd9c47-5fa3-45bb-8668-7789a0e26d0b",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-10-30 16:11:05.134 No runtime found, using MemoryCacheStorageManager\n",
      "2025-10-30 16:11:05.139 No runtime found, using MemoryCacheStorageManager\n"
     ]
    }
   ],
   "source": [
    "@st.cache_data(show_spinner=False)\n",
    "def get_covid_data():\n",
    "    url = \"https://disease.sh/v3/covid-19/historical/all?lastdays=365\"\n",
    "    res = requests.get(url)\n",
    "    data = res.json()\n",
    "\n",
    "    df = pd.DataFrame({\n",
    "        \"Date\": list(data[\"cases\"].keys()),\n",
    "        \"Confirmed\": list(data[\"cases\"].values()),\n",
    "        \"Deaths\": list(data[\"deaths\"].values()),\n",
    "        \"Recovered\": list(data[\"recovered\"].values())\n",
    "    })\n",
    "    df[\"Date\"] = pd.to_datetime(df[\"Date\"])\n",
    "    return df\n",
    "@st.cache_data(show_spinner=False)\n",
    "def get_economic_data(country_code=\"IN\"):\n",
    "    indicators = {\n",
    "        \"GDP\": \"NY.GDP.MKTP.CD\",\n",
    "        \"Unemployment\": \"SL.UEM.TOTL.ZS\"\n",
    "    }\n",
    "\n",
    "    econ_data = {}\n",
    "    for key, indicator in indicators.items():\n",
    "        url = f\"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json&per_page=100\"\n",
    "        resp = requests.get(url).json()\n",
    "        if len(resp) > 1:\n",
    "            econ_data[key] = pd.DataFrame(resp[1])[[\"date\", \"value\"]].rename(columns={\"date\": \"Year\", \"value\": key})\n",
    "    merged = pd.merge(econ_data[\"GDP\"], econ_data[\"Unemployment\"], on=\"Year\", how=\"outer\")\n",
    "    merged = merged.dropna().sort_values(\"Year\")\n",
    "    merged[\"Year\"] = merged[\"Year\"].astype(int)\n",
    "    merged[\"Country\"] = country_code\n",
    "    return merged\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "dd38e95f-f3d5-4e7b-bed1-f15bf64e4d95",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-10-30 16:11:16.809 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:11:16.812 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:11:16.814 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:11:16.815 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:11:16.817 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:11:16.818 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:11:16.819 Session state does not function when running a script without `streamlit run`\n",
      "2025-10-30 16:11:16.821 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:11:16.823 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:11:16.825 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:11:16.829 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:11:16.829 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:11:16.835 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:11:16.837 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "with st.sidebar:\n",
    "    st.header(\"⚙️ Dashboard Controls\")\n",
    "    country_code = st.text_input(\"Enter Country ISO Code (e.g., IN, US, CN):\", \"IN\").upper()\n",
    "    refresh = st.button(\"🔄 Refresh Data\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "dc9877f0-f375-4278-8212-a8b351f7cc9d",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-10-30 16:11:27.777 No runtime found, using MemoryCacheStorageManager\n",
      "C:\\Users\\jinda\\AppData\\Local\\Temp\\ipykernel_19864\\928184829.py:13: UserWarning: Could not infer format, so each element will be parsed individually, falling back to `dateutil`. To ensure parsing is consistent and as-expected, please specify a format.\n",
      "  df[\"Date\"] = pd.to_datetime(df[\"Date\"])\n",
      "2025-10-30 16:11:30.278 No runtime found, using MemoryCacheStorageManager\n",
      "2025-10-30 16:11:33.432 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:11:33.432 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "covid_df = get_covid_data()\n",
    "econ_df = get_economic_data(country_code)\n",
    "\n",
    "st.caption(f\"📅 Data last updated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "a5cfefb8-0f7f-4ad2-b74b-6f98ab9c3433",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-10-30 16:12:24.323 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:24.325 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:24.325 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:24.325 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:24.332 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "C:\\Users\\jinda\\anaconda3\\Lib\\site-packages\\_plotly_utils\\basevalidators.py:106: FutureWarning: The behavior of DatetimeProperties.to_pydatetime is deprecated, in a future version this will return a Series containing python datetime objects instead of an ndarray. To retain the old behavior, call `np.array` on the result\n",
      "  v = v.dt.to_pydatetime()\n",
      "2025-10-30 16:12:26.133 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:26.133 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:26.141 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:26.146 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:26.155 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:26.159 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:26.278 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:26.278 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:26.281 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:26.281 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:26.284 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:26.286 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:26.403 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:26.403 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:26.414 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:26.415 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:26.415 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:26.415 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "col1, col2 = st.columns(2)\n",
    "\n",
    "# COVID Trend\n",
    "with col1:\n",
    "    st.subheader(\"🦠 COVID-19 Global Trend (Last 12 Months)\")\n",
    "    covid_fig = px.line(\n",
    "        covid_df, x=\"Date\", y=[\"Confirmed\", \"Recovered\", \"Deaths\"],\n",
    "        title=f\"COVID-19 Global Trend\",\n",
    "        markers=True, template=\"plotly_white\"\n",
    "    )\n",
    "    st.plotly_chart(covid_fig, use_container_width=True)\n",
    "    \n",
    "# Economic Indicators\n",
    "with col2:\n",
    "    st.subheader(f\"💹 Economic Indicators — {country_code}\")\n",
    "    econ_fig = px.line(\n",
    "        econ_df, x=\"Year\", y=[\"GDP\", \"Unemployment\"],\n",
    "        title=f\"GDP & Unemployment Trends ({country_code})\",\n",
    "        markers=True, template=\"plotly_white\"\n",
    "    )\n",
    "    st.plotly_chart(econ_fig, use_container_width=True)\n",
    "\n",
    "# Correlation Analysis\n",
    "st.subheader(\"📊 GDP vs COVID Impact\")\n",
    "merged = econ_df.copy()\n",
    "merged[\"Confirmed\"] = covid_df[\"Confirmed\"].iloc[-len(merged):].values\n",
    "corr_fig = px.scatter(\n",
    "    merged, x=\"GDP\", y=\"Confirmed\",\n",
    "    size=\"Unemployment\", color=\"Year\",\n",
    "    title=f\"GDP vs COVID Confirmed Cases ({country_code})\",\n",
    "    template=\"plotly_white\"\n",
    ")\n",
    "st.plotly_chart(corr_fig, use_container_width=True)\n",
    "\n",
    "st.success(\"✅ Dashboard ready! Data fetched live from World Bank & disease.sh APIs.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "54219f8d-8736-4da9-922e-2486b4dfe25a",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-10-30 16:12:43.798 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:43.807 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:43.809 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-10-30 16:12:43.810 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# ---------------------- Footer ----------------------\n",
    "st.markdown(\"---\")\n",
    "st.markdown(\"**Created by [Mahi Jindal](https://www.linkedin.com/in/mahi-jindal)** | GitHub: [18mahi](https://github.com/18mahi)\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "45221efd-1ad0-46c2-95ee-2b085ed3cf5c",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
