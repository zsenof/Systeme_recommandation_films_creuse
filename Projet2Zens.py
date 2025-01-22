import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors


#Lecture du fichier
data = pd.read_csv("df_clean.csv", sep=";")
df= pd.DataFrame(data)

features = ['startYear', 'runtimeMinutes', 'averageRating', 'genre_numeric']

# normalisation des données

scaler = MinMaxScaler()

X_scaled = scaler.fit_transform(df[features])

# transformation en dataframe
df_scal = pd.DataFrame(X_scaled, columns= ['startYear', 'runtimeMinutes', 'averageRating', 'genre_numeric'], index = df['original_title'])

# Initiation du modèle NearestNeighbors

knn = NearestNeighbors(n_neighbors=4, metric='cosine')
knn.fit(df_scal)

metric = 'cosine'




# ========================
# Page principale
# ========================

def accueil():
    
    st.markdown("<h1 style='text-align: center;color:black;'>Projet Cinéma en Creuse</h1>", unsafe_allow_html=True)
    
    st.image("Image/Image_cinema.jpg",  width= 650) 
    
    colA, colB, colC = st.columns(3)
    with colA:
        st.image("Image/Logo Zens.jpg",width=200) 
    
    with colB:
        st.image("Image/Logo WCS.jpg",width=600) 
    st.write("   ")
    st.write("   ")
    st.write("   ")


def page_presentation():
    st.markdown("<h1 style='text-align: center;color:black;'>Présentation du Projet</h1>", unsafe_allow_html=True)
    st.text("\n\n\n")
    
    st.markdown(
        '<p style="font-size:20px;">Un cinéma en perte de vitesse situé dans la Creuse nous a contacté. Il a décidé de passer le cap du digital en créant un site Internet taillé pour les locaux. Il nous a demandé de créer un moteur de recommandations de films.</p>',
        unsafe_allow_html=True)
    
    st.write("  ")   
    
    st.markdown(
        '<h2 style="font-size: 25px;">Pour réaliser ce projet, nous avons utilisé les outils suivants :</h2>',
        unsafe_allow_html=True
    )
    
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    outils = [("Airtable", "Image/Logo Airtable.jpg"), ("Scikit-Learn", "Image/sklearn_logo.png"), ("Slack", "Image/logo-Slack-1.webp"), ("Streamlit", "Image/Logo streamlit.jpg"),("Python", "Image/Logo Python-Symbole.jpg") , ("Pandas", "Image/Pandas_logo.svg.png"), ("Canva", "Image/Canva-Nouveau-Logo.jpg") ]   
    for col, (nom, image) in zip([col1, col2, col3, col4, col5, col6, col7], outils):
        with col:
            st.image(image, width=100)     

def page_etude():
    st.markdown("<h1 style='text-align: center;color:black;'>Etude de marché</h1>", unsafe_allow_html=True)
    st.text("\n\n\n")
    st.markdown(
        '<p style="font-size:20px;">Voir la présentation GoogleSlide remise au client.</p>',
        unsafe_allow_html=True)
    st.write("  ")   

def page_KPI():
    st.markdown("<h1 style='text-align: center;color:black;'>Présentation des KPI</h1>", unsafe_allow_html=True)
    st.text("\n\n\n")
    st.write("Nous avons retenu les 4 KPI suivants :")
    st.image("KPI.jpg")

def page_outil_recommandation():
    st.markdown("<h1 style='text-align: center;color:black;'>Outil de recommandation de films</h1>", unsafe_allow_html=True)
    st.text("\n\n\n")
    genres = ["Sélectionnez un genre", "Drama", "Comedy,Drame"]
    selected_genres = st.selectbox("Quel genre de films recherchez-vous ?", genres)

    selected_periode = st.selectbox(
        "Quelle période de sortie ciblez-vous ?", 
        ["Sélectionnez une période", "Années 1960", "Années 1970", "Films récents : 2022-2024"]
    )

    # Listes des périodes
    annees60 = list(range(1960, 1970))
    annees70 = list(range(1970, 1980))
    annees2224 = [2022, 2023, 2024]

    choix_annee = []

    if selected_periode == "Années 1960":
        choix_annee = annees60
    elif selected_periode == "Années 1970":
        choix_annee = annees70
    elif selected_periode == "Films récents : 2022-2024":
        choix_annee = annees2224

    if not choix_annee:
        st.write("Veuillez sélectionner une période valide.")
        return

    # Filtrage des films
    movies = df["original_title"][
        df["genres"].str.contains(selected_genres, case=False, na=False) & 
        df["startYear"].isin(choix_annee)
    ]

    if selected_periode != "Sélectionnez une période" and selected_genres != "Sélectionnez un genre":
        selected_movie = st.selectbox("Quel film avez vous apprécié parmi les suivants ?", movies)
        nom_film_test = selected_movie
    else:
        st.write("Veuillez sélectionner un genre et une période.")
        return

    # Recommandation
    if nom_film_test in df_scal.index:
        nom_film_test_index = df_scal.index.get_loc(nom_film_test)
        distances, indices = knn.kneighbors(df_scal.iloc[[nom_film_test_index]])

        films_similaires = []
        for distance, index in zip(distances[0][1:], indices[0][1:]):
            film_similaire = df_scal.index[index]
            films_similaires.append(film_similaire)

        if len(films_similaires) >= 3:
            preco_1 = films_similaires[0]
            preco_2 = films_similaires[1]
            preco_3 = films_similaires[2]


        else:
            st.write("Pas assez de films similaires trouvés pour effectuer une recommandation.")
    else:
        st.write(f"Le film '{nom_film_test}' n'existe pas dans la base de données.")

    st.write("  ")
    st.write("  ")

    st.markdown(
            '<p style="font-size:25px;">Voici notre proposition de films :</p>',
        unsafe_allow_html=True)
        
        # MACHINE LEARNING #
    

    base_url_tmdb = "https://image.tmdb.org/t/p/w500"
    term_url1 = df.loc[df['original_title'] == preco_1, 'poster_path'].values[0]
    term_url2 = df.loc[df['original_title'] == preco_2, 'poster_path'].values[0]
    term_url3 = df.loc[df['original_title'] == preco_3, 'poster_path'].values[0]

    image1 = base_url_tmdb+term_url1
    image2 = base_url_tmdb+term_url2
    image3 = base_url_tmdb+term_url3

    titre1 = preco_1
    titre2 = preco_2
    titre3 = preco_3

    note1 = df.loc[df['original_title'] == preco_1, 'averageRating'].values[0]
    note2 = df.loc[df['original_title'] == preco_2, 'averageRating'].values[0]
    note3 = df.loc[df['original_title'] == preco_3, 'averageRating'].values[0]


    realisateur1 = df.loc[df['original_title'] == preco_1, 'director'].values[0]
    realisateur2 = df.loc[df['original_title'] == preco_2, 'director'].values[0]
    realisateur3 = df.loc[df['original_title'] == preco_3, 'director'].values[0]

    acteurs1 = df.loc[df['original_title'] == preco_1, 'acteurs/trice'].values[0]
    acteurs2 = df.loc[df['original_title'] == preco_2, 'acteurs/trice'].values[0]
    acteurs3 = df.loc[df['original_title'] == preco_3, 'acteurs/trice'].values[0]

    description1 = df.loc[df['original_title'] == preco_1, 'overview_fr'].values[0]
    description2 = df.loc[df['original_title'] == preco_2, 'overview_fr'].values[0]
    description3 = df.loc[df['original_title'] == preco_3, 'overview_fr'].values[0]

    col1, col2 = st.columns(2)

    with col1:
            st.image(image1)
    with col2:
        st.header(titre1)
        st.write(f"**Note** : {note1}")
        st.write(f"**Réalisateur** : {realisateur1}")
        st.write(f"**Acteurs et Actrices** : {acteurs1}")
        st.write(f"**Description du film** : {description1}")
    #video1 = "https://youtu.be/APv2lidaDmo"
    #st.video(video1)

    st.write("-----------------------------------------------------------------")

    col3, col4 = st.columns(2)

    with col3:
        st.image(image2)
    with col4:
        st.header(titre2)
        st.write(f"**Note** : {note2}")
        st.write(f"**Réalisateur** : {realisateur2}")
        st.write(f"**Acteurs et Actrices** : {acteurs2}")
        st.write(f"**Description du film** : {description2}")

    st.write("-----------------------------------------------------------------")

    col5, col6 = st.columns(2)

    with col5:
        st.image(image3)
    with col6:
        st.header(titre3)
        st.write(f"**Note** : {note3}")
        st.write(f"**Réalisateur** : {realisateur3}")
        st.write(f"**Acteurs et Actrices** : {acteurs3}")
        st.write(f"**Description du film** : {description3}")

    st.write("-----------------------------------------------------------------")




def axes_amelioration():
    st.markdown("<h1 style='text-align: center;color:black;'>Axes d'amélioration</h1>", unsafe_allow_html=True)
    st.write(" ")
    st.write("Afin d'améliorer l'outil, il sera utile de :")
    st.write("     1- Faire bla bla bla ")
    st.write("     2- Faire bla bla bla ")
    st.write("     3- Faire bla bla bla ")
    st.write("     4- Faire bla bla bla ")
    st.image("Image/Logo Zens.jpg", width=200)










# ========================
# Barre latérale
# ========================

st.sidebar.title("")
    
st.sidebar.image("Image/Logo le Senechal.jpg")
st.sidebar.write(" ")
st.sidebar.write(" ")
st.sidebar.write(" ")

    # Choix de l'affichage : 
affichage_sel  = st.sidebar.radio(
        "Sommaire",
        ["Accueil", "Présentation du Projet", "Outil de Recommandation", "Dataframe"]
    )

# ["Accueil", "Présentation du Projet", "Etude de Marché", "KPI", "Outil de Recommandation","Axes d'Amélioration", "Dataframe"]

if affichage_sel == "Accueil":
        accueil()
        
if affichage_sel == "Présentation du Projet":
        page_presentation()
        
if affichage_sel == "Etude de Marché":
        page_etude()

if affichage_sel == "KPI":
        page_KPI()
  

if affichage_sel == "Outil de Recommandation":
        page_outil_recommandation()
  

if affichage_sel == "Axes d'Amélioration":
        axes_amelioration()
  
if affichage_sel == "Dataframe":
    st.image("Stats_dataframe.jpg")  
    df

    # lancer le code    streamlit run Projet2Zens.py
