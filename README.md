# Analyse et prévision de la concentration de CO2

Ce projet analyse l'évolution hebdomadaire de la concentration de CO2 mesurée à
l'observatoire de Mauna Loa, à Hawaï. Il comprend un notebook d'analyse et un
dashboard interactif développé avec Streamlit.

## Fonctionnalités

- Visualisation des mesures historiques et de l'autocorrélation de la série.
- Affichage du diagnostic des résidus du modèle.
- Visualisation des prévisions et de leur intervalle.
- Sélection d'une date pour consulter la prévision correspondante.

Les prévisions du dashboard sont pré-calculées et enregistrées dans
`future_forecasts.pkl`. Le sélecteur de date consulte ces valeurs; il ne réajuste
pas le modèle à chaque utilisation.

## Données et méthode

Les observations hebdomadaires couvrent la période du 29 mars 1958 au
17 octobre 2026. Elles proviennent du programme CO2 de Scripps, à l'Université
de Californie à San Diego :
[données hebdomadaires de Mauna Loa](https://scrippsco2.ucsd.edu/data/atmospheric-co2-data/sampling-station-records/mauna-loa-observatory-hawaii/).

Le dashboard présente un modèle SARIMA(3,1,3)(1,1,2,52), avec une saisonnalité
annuelle de 52 semaines. Le diagnostic disponible indique que le test de
Ljung-Box ne met pas en évidence d'autocorrélation des résidus (p = 0,55), mais
que le test de Jarque-Bera rejette leur normalité (p < 0,001). Ces tests ne
garantissent pas à eux seuls la qualité des prévisions.

Les prévisions enregistrées couvrent 520 semaines, du 24 octobre 2026 au
4 octobre 2036. Elles sont issues d'un modèle de série temporelle et ne
représentent pas des scénarios d'émissions.

## Fichiers du projet

| Fichier | Description |
| --- | --- |
| `dashbord.py` | Application Streamlit |
| `co2_concentration.ipynb` | Analyse des données et modélisation |
| `co2_weekly_mlo.csv` | Observations historiques hebdomadaires |
| `diagnostic.png` | Graphique de diagnostic affiché dans le dashboard |
| `future_forecasts.pkl` | Prévisions précalculées et bornes de l'intervalle |
| `co2_model_light.pkl` | Paramètres sauvegardés du modèle pour le notebook |


## Installation et lancement

Python 3.12 est utilisé pour le développement du projet.

Sous Windows, depuis le dossier du projet :

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirement.txt
streamlit run dashbord.py
```

Le dashboard s'ouvre ensuite dans le navigateur. Les fichiers de données et
les artefacts nécessaires (`co2_weekly_mlo.csv`, `diagnostic.png` et
`future_forecasts.pkl`) doivent être présents à la racine du projet.

## Reproductibilité

Le notebook documente les étapes d'analyse et de modélisation. Les prévisions
affichées par le dashboard sont des artefacts pré-calculés : modifier le CSV ne
met pas automatiquement à jour le modèle ni les prévisions. Pour actualiser
les résultats, il faut réexécuter les étapes de modélisation du notebook puis
remplacer les artefacts correspondants.
