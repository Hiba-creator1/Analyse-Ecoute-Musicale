import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
os.makedirs("graphiques", exist_ok=True)

df = pd.read_csv("ecoute_musique.csv")
#1. préparation et nettoyage
#convertir les colonnes date et heure _ecoute en datetime:
df["date"]=pd . to_datetime(df["date"])
df['heure_ecoute']=pd.to_datetime(df ["heure_ecoute"])

#création des nouveaux colonnes
df['jour_semaine']=df["date"].dt.day_name()
df['heure_arrondie']= df['heure_ecoute'].dt.hour

#vérification des doublons:
print("Nombre de doublons :", df.duplicated().sum())
print("Lignes doublons :")
print(df[df.duplicated()])

#identifier et traiter les doublons:
print("Valeurs manquantes par colonne :")
print(df.isnull().sum())
df['duree'] = df['duree'].fillna(df['duree'].mean())
df = df.dropna(subset=['plateforme', 'genre'])
print("Dimensions du DataFrame après nettoyage :", df.shape)
print("Aperçu des données nettoyées :")
print(df.head())

# 2.analyse temporelle:
#répartition des écoutes par heure de la journée
ecoutes_par_heure = df['heure_arrondie'].value_counts().sort_index()
plt.figure(figsize=(10,5))
plt.plot(ecoutes_par_heure.index, ecoutes_par_heure.values, marker='o')
plt.title("Répartition des écoutes par heure de la journée")
plt.xlabel("Heure")
plt.ylabel("Nombre d'écoutes")
plt.grid(True)
plt.savefig("graphiques/ecoutes_par_heure.png")
plt.show()

#répartition des écoutes par jour de la semaine:
jours_ordre = ["Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"]
ecoutes_par_jour = df['jour_semaine'].value_counts().reindex(jours_ordre)
plt.figure(figsize=(9,6))
sns.barplot(x=ecoutes_par_jour.index, y=ecoutes_par_jour.values, palette="viridis")
plt .title ("Répartition des écoutes par jour de la semaine")
plt.xlabel("Jour ")
plt.ylabel(" Nombre d'écoutes")
plt.xticks(rotation=45)
plt.savefig("graphiques/ecoutes_par_jour.png")
plt.show()

#heatmap croisant jours et heures d'écoute
jours_ordre = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
heatmap_data = df.pivot_table(
    index='jour_semaine',
    columns='heure_arrondie',
    values='titre_morceau',
    aggfunc='count',
    fill_value=0
)
heatmap_data = heatmap_data.reindex(jours_ordre)
plt.figure(figsize=(12,6))
sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt="d")
plt.title("Heatmap des écoutes par jour et par heure")
plt.xlabel("Heure de la journée")
plt.ylabel("Jour de la semaine")
plt.savefig("graphiques/heatmap_ecoutes.png")
plt.show()

#3.analyse des préférences musicales 
#genre le plus écoute
genre_total = df.groupby("genre")[ 'duree'].sum()
print(" minutes écoutées par genre :")
print(genre_total)
print("\nGenre le plus écouté :")
print(genre_total.idxmax())
plt.figure(figsize=(8,5))
plt.pie(
    genre_total,
    labels=genre_total.index,
    autopct='%1.1f%%',
    startangle=90
)
plt.title("Répartition des genres musicaux")
plt.savefig("graphiques/repartition_genres.png")
plt.show()

#genre préférée par plateforme
plateformes = df["plateforme"].unique()
genres_pref = []
noms_plateformes = []
print("\nGenre préféré par plateforme :")
for plateforme in plateformes:
    data = df[df["plateforme"] == plateforme]
    total = data.groupby("genre")['duree'].sum()
    genre_pref = total.idxmax()
    print(plateforme, ":", genre_pref)
    noms_plateformes.append(plateforme)
    genres_pref.append(total.max())
plt.figure(figsize=(9,4))
plt.bar(noms_plateformes, genres_pref, color="orange")
plt.title("Genre préféré par plateforme")
plt.xlabel("Plateforme")
plt.ylabel("Minutes écoutées")
plt.savefig("graphiques/genre_prefere_plateforme.png")
plt.show()

#heure la plus fréquente pour écouter chaque genre:
df['heure'] = pd.to_datetime(df['heure_ecoute']).dt.hour
freq_hours = df.groupby('genre')['heure'].agg(lambda x: x.mode()[0])
print("\nHeure la plus fréquente par genre :")
print(freq_hours)
freq_hours.plot(kind='bar', color='green')
plt.title("Heure la plus fréquente par genre")
plt.xlabel("Genre")
plt.ylabel("Heure (0–23)")
plt.savefig("graphiques/heure_frequente_genre.png")
plt.show() 

#comparaison de la durée moyenne d'écoute selon les genres:
duree_moyenne = df.groupby('genre')['duree'].mean()
print("\nDurée moyenne d'écoute par genre :")
print(duree_moyenne)
duree_moyenne.plot(kind='bar', color='orange')
plt.title("Durée moyenne d'écoute par genre")
plt.xlabel("Genre")
plt.ylabel("Durée moyenne (minutes)")
plt.savefig("graphiques/duree_moyenne_genre.png")
plt.show()

#4-analyse des plateformes
# Total de minutes écoutées par platefome
minutes_plateforme = df.groupby("plateforme")["duree"].sum()
print("Total des minutes par plateforme :")
print(minutes_plateforme)
minutes_plateforme.plot(kind="bar")
plt.title("Minutes totales par plateforme")
plt.xlabel("Plateforme")
plt.ylabel("Minutes")
plt.savefig("graphiques/minutes_plateforme.png")
plt.show()

#Durée moyenne d'une session par plateforme
moyenne_duree = df.groupby("plateforme")["duree"].mean()
print("\nDurée moyenne par plateforme :")
print(moyenne_duree)
moyenne_duree.plot(kind="bar")
plt.title("Durée moyenne des sessions")
plt.xlabel("Plateforme")
plt.ylabel("Durée moyenne")
plt.savefig("graphiques/duree_moyenne_sessions.png")
plt.show()

# Plateforme la plus utilisée le week-end
df["date"] = pd.to_datetime(df["date"])
df["jour_semaine"] = df["date"].dt.day_name()
weekend = df[
    (df["jour_semaine"] == "Saturday") |
    (df["jour_semaine"] == "Sunday")
]
plateforme_weekend = weekend["plateforme"].value_counts()
print("\nPlateforme la plus utilisée le week-end :")
print(plateforme_weekend)
plateforme_weekend.plot(kind="bar")
plt.title("Utilisation des plateformes le week-end")
plt.xlabel("Plateforme")
plt.ylabel("Nombre d'écoutes")
plt.savefig("graphiques/plateforme_weekend.png")
plt.show()

# Morceaux les plus populaires par plateforme
print("\nMorceaux les plus populaires :")
plateformes = df["plateforme"].unique()
for p in plateformes:
    print("\nPlateforme :", p)
    top_morceaux = (
        df[df["plateforme"] == p]["titre_morceau"]
        .value_counts()
        .head(3)
    )
    print(top_morceaux)

#  Nombre de sessions > 8 minutes par plateforme
sessions_longues = df[df["duree"] > 8]
nb_sessions = sessions_longues["plateforme"].value_counts()
print("\nNombre de sessions > 8 minutes :")
print(nb_sessions)
nb_sessions.plot(kind="bar")
plt.title("Sessions de plus de 8 minutes")
plt.xlabel("Plateforme")
plt.ylabel("Nombre de sessions")
plt.savefig("graphiques/sessions_longues.png")
plt.show()

#5.expoert et synthése
resultats = pd.DataFrame({
    "minutes_totales": minutes_plateforme,
    "duree_moyenne": moyenne_duree
})

resultats.to_csv("resultats_ecoute.csv", index=True)