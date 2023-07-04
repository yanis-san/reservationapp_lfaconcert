import sqlite3
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader




# Créer une connexion à la base de données
conn = sqlite3.connect("tickets.db")
c = conn.cursor()

def delete_data(ids):
    # Vérifier si la base de données contient des enregistrements
    c.execute("SELECT COUNT(*) FROM clients")
    count = c.fetchone()[0]

    if count > 0:
        # Supprimer les enregistrements de la base de données en utilisant les IDs fournis
        for id in ids:
            c.execute("DELETE FROM clients WHERE id=?", (id,))
        conn.commit()
    else:
        st.warning("La base de données est vide.")

def show_database_data():
    st.title("Base de données des clients")

    # Récupérer les données de la base de données
    c.execute("SELECT id, name, email, phone, age, gender, timestamp FROM clients")
    rows = c.fetchall()

    # Vérifier si la base de données est vide
    if not rows:
        st.warning("La base de données est vide.")
        return

    # Afficher les données dans un DataFrame
    df = pd.DataFrame(rows, columns=["ID", "Nom", "Email", "Numéro de téléphone", "Âge", "Sexe", "Date et heure"])

    # Afficher les champs d'entrée pour les IDs à supprimer
    delete_ids = st.text_input(" Saisissez les personnes à supprimer (IDs séparés par des virgules)", "")

    # Vérifier si le bouton "Supprimer (Entrée)" a été cliqué
    delete_button_clicked = st.button("Supprimer (Entrée)", key="delete_button")

    if delete_button_clicked:
        # Convertir les IDs saisis en une liste d'entiers
        ids_to_delete = [int(id.strip()) for id in delete_ids.split(",") if id.strip().isdigit()]

        # Vérifier si la base de données contient des enregistrements avant la suppression
        c.execute("SELECT COUNT(*) FROM clients")
        count = c.fetchone()[0]

        if count > 0:
            # Supprimer les enregistrements correspondants dans la base de données lorsque les IDs sont saisis
            delete_data(ids_to_delete)
            st.success("Donnée(s) supprimée(s) avec succès")
        else:
            st.warning("La base de données est vide.")

    # Mettre à jour les données du DataFrame après la suppression
    c.execute("SELECT id, name, email, phone, age, gender, timestamp FROM clients")
    rows = c.fetchall()
    df = pd.DataFrame(rows, columns=["ID", "Nom", "Email", "Numéro de téléphone", "Âge", "Sexe", "Date et heure"])

    # Vérifier si le DataFrame est vide après la suppression
    if df.empty:
        st.warning("La base de données est vide.")
        return

    # Afficher le DataFrame mis à jour
    st.dataframe(df)

    # Répartition des genres
    st.subheader("Répartition des sexes")
    gender_counts = df["Sexe"].value_counts()

    if not gender_counts.empty:
        fig, ax = plt.subplots()
        sns.barplot(x=gender_counts.index, y=gender_counts.values, ax=ax)
        plt.xlabel("Sexe")
        plt.ylabel("Nombre de clients")
        st.pyplot(fig)
    else:
        st.warning("Aucune donnée de sexe disponible pour afficher le graphique.")

    # Répartition des âges
    st.subheader("Répartition des âges")
    fig, ax = plt.subplots()
    sns.histplot(data=df, x="Âge", bins=20, kde=True, ax=ax)
    plt.xlabel("Âge")
    plt.ylabel("Nombre de clients")
    st.pyplot(fig)



st.title("Login")
tentative_pass=st.text_input("Password",type="password")

if tentative_pass:
    if tentative_pass==st.secrets["SECRET_KEY"]:
        show_database_data()
    else:
        st.warning("Mot de passe incorrect")
    
        


