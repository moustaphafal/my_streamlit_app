import streamlit as st

def sidebar_navigation():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choisissez une vue :",
        (
            "Aperçu des données",
            "Statistiques",
            "Transactions par catégorie",
            "Transactions par pays",
            "Transactions par devise",
            "Transactions par client",
            "Transactions dans le temps",
            "Détection de fraude"
        )
    )
    return page
