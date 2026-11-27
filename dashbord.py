import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
## bibliothèques pour gérer les timeseries
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import joblib
from pathlib import Path

## Informations générales sur le projet
st.title("Analyse de la concentration de CO2")
st.header("A propos du projet")
st.markdown("""
Ce projet vise à analyser la concentration de CO2 dans l'atmosphère au fil du temps, en utilisant des données historiques et des modèles statistiques pour prévoir les tendances futures. L'objectif est de sensibiliser à l'impact du CO2 sur le changement climatique et d'explorer les implications pour l'environnement.
""")
st.header("Données utilisées")
st.markdown("""Le jeu de données couvre la période de 1958 à la semaine 42 de l'année 2026, avec une dernière observation enregistrée le 17 octobre 2026. Les observations sont hebdomadaires et proviennent du site de l'Université de Californie à San Diego (UC San Diego) : [données](https://scrippsco2.ucsd.edu/data/atmospheric-co2-data/sampling-station-records/mauna-loa-observatory-hawaii/). 
La concentration de co2 est exprimé en micro-mol par moles (ppm). Voici un aperçu des données utilisées dans ce projet :""")
# Importation des données
parent_file_path = Path(__file__).parent 
data = pd.read_csv(parent_file_path / 'co2_weekly_mlo.csv', comment='"', header=None, names=["date", "co2"])
st.write(data.head(10))

## Conversion de la colonne "date" en type datetime
data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
fig,ax = plt.subplots(figsize=(12,6))
data.plot(x='date', y='co2', ax=ax)
plt.title('Concentration de CO2 à Mauna Loa (Hawaï) - Données hebdomadaires')
plt.xlabel('Date')
plt.ylabel('Concentration de CO2 (ppm)')
st.pyplot(fig)
st.caption("Figure 1 : Concentration de CO2 - Données hebdomadaires")
st.markdown(""" L'analyse du graphique met en évidence une tendance à la hausse ainsi qu'une saisonnalité a priori additive de la concentration de CO2 dans l'atmosphère depuis 1960. 
Pour identifier la période saisonnière, nous retirerons d'abord la tendance de la série, puis nous examinerons sa fonction d'autocorrélation (ACF). Nous partirons de l'hypothèse d'une saisonnalité annuelle, soit une période de 52 semaines.""")

# detrending the data to remove the seasonal component
data['co2_detrended'] = data['co2'] - data['co2'].rolling(window=52).mean()
fig, ax = plt.subplots(figsize=(12,6))
plot_acf(data['co2_detrended'].dropna(), lags=100, ax=ax)
plt.xlabel('Lags (semaines)')
plt.ylabel('Autocorrélation')
st.pyplot(fig)
st.caption("Figure 2 : Fonction d'autocorrélation (ACF) de la série temporelle de CO2 après suppression de la tendance")

st.header("Diagnostic des résidus")
st.image(parent_file_path / 'diagnostic.png', caption="Figure 3 : Diagnostic des résidus du modèle SARIMA(3,1,3)(1,1,2,52)")
st.markdown(
    "Le test de Ljung-Box ne met pas en évidence d'autocorrélation des résidus "
    "(p = 0,55). En revanche, le test de Jarque-Bera rejette leur normalité "
    "(p < 0,001)."
)


st.header("Prévision de la concentration de CO2")
st.markdown("""Pour prévoir la concentration de CO2, nous avons utilisé le modèle SARIMA(3,1,3)(1,1,2,52), qui est un modèle de séries temporelles adapté aux données saisonnières. 
Le modèle a été ajusté aux données historiques et utilisé pour générer des prévisions futures. 
Pour démontrer les résultats du modèle, nous allons afficher les prévisions pour les 10 prochaines semaines, ce qui correspond à la période allant de 24 Oct 2026 au 26 Dec 2026.""")

# Processing the data for SARIMAX model
co2_weekly = data.set_index('date')['co2']
#co2_weekly = co2_weekly.asfreq('W-SAT')

forecast_df = joblib.load(parent_file_path / "future_forecasts.pkl")

pred = forecast_df.iloc[0:10, :]  # Select the first 10 weeks of forecasts
st.write("Prévisions de la concentration de CO2 pour les 10 prochaines semaines :")
st.write(pred.head(10))


fig, ax = plt.subplots(figsize=(12,6))

co2_weekly['2026'].plot(ax=ax, label="Observé")
pred.set_index('date', inplace=True)
pred.plot(ax=ax, color="red", label=("mean","lower","upper"))
plt.xlabel('Date')
plt.ylabel('Concentration de CO2 (ppm)')
plt.title('Prévisions de la concentration de CO2')
plt.legend()
st.pyplot(fig)

## simulation module
st.sidebar.header("Simulation de la concentration de CO2")
st.sidebar.markdown(
    "Choisissez une date puis cliquez sur Simuler pour afficher la prévision "
    "et son intervalle."
)
forecast_dates = forecast_df["date"].tolist()
selected_date = st.sidebar.select_slider(
    "Date de prévision",
    options=forecast_dates,
    value=forecast_dates[0],
    format_func=lambda date: date.strftime("%Y-%m-%d"),
)

if st.sidebar.button("Simuler"):
    selected_forecast = forecast_df.loc[forecast_df["date"] == selected_date].iloc[0]
    st.sidebar.subheader(f"Prévision pour le {selected_date:%d/%m/%Y}")
    st.sidebar.metric(
        "Concentration prévue",
        f"{selected_forecast['forecast']:.2f} ppm",
    )
    st.sidebar.caption(
        "Intervalle de prévision : "
        f"{selected_forecast['lower']:.2f} à "
        f"{selected_forecast['upper']:.2f} ppm"
    )

