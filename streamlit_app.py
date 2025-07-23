import pandas as pd
import streamlit as st

st.title("📊 Dashboard des Transactions")

# Charger les données
csv_file = "Transactions_data_complet.csv"
df = pd.read_csv(csv_file)

# Nettoyage des données
# Suppression des doublons
df = df.drop_duplicates()
# Suppression des lignes entièrement vides
df = df.dropna(how='all')
# Suppression des colonnes entièrement vides
df = df.dropna(axis=1, how='all')
# Remplacement des valeurs manquantes par 0 pour la colonne Amount si elle existe
if 'Amount' in df.columns:
    df['Amount'] = df['Amount'].fillna(0)
# Nettoyage des dates si la colonne existe
if 'TransactionStartTime' in df.columns:
    df['TransactionStartTime'] = pd.to_datetime(df['TransactionStartTime'], errors='coerce')

# Sauvegarde du fichier nettoyé
cleaned_file = csv_file.replace('.csv', '_cleaned.csv')
df.to_csv(cleaned_file, index=False)
st.success(f"Fichier nettoyé sauvegardé sous : {cleaned_file}")

# Filtres interactifs
provider_options = df['ProviderId'].dropna().unique() if 'ProviderId' in df.columns else []
selected_providers = st.sidebar.multiselect("Filtrer par ProviderId", provider_options) if len(provider_options) > 0 else []

if 'TransactionStartTime' in df.columns:
    min_date = df['TransactionStartTime'].min()
    max_date = df['TransactionStartTime'].max()
    selected_dates = st.sidebar.date_input("Filtrer par date de transaction", [min_date, max_date], min_value=min_date, max_value=max_date)
else:
    selected_dates = None

# Application des filtres
filtered_df = df.copy()
if selected_providers:
    filtered_df = filtered_df[filtered_df['ProviderId'].isin(selected_providers)]
if selected_dates and isinstance(selected_dates, list) and len(selected_dates) == 2:
    start, end = pd.to_datetime(selected_dates[0]), pd.to_datetime(selected_dates[1])
    filtered_df = filtered_df[(filtered_df['TransactionStartTime'] >= start) & (filtered_df['TransactionStartTime'] <= end)]

st.subheader("Aperçu des données filtrées")
st.dataframe(filtered_df)

st.subheader("Statistiques de base")
total_transactions = len(filtered_df)
total_amount = filtered_df['Amount'].sum() if 'Amount' in filtered_df.columns else None
st.metric("Nombre total de transactions", total_transactions)
if total_amount is not None:
    st.metric("Montant total des transactions", f"{total_amount:,.2f}")

if 'ProductCategory' in filtered_df.columns:
    st.subheader("Transactions par catégorie")
    st.bar_chart(filtered_df['ProductCategory'].value_counts())

if 'CustomerId' in filtered_df.columns and 'Amount' in filtered_df.columns:
    st.subheader("Transactions par client")
    st.bar_chart(filtered_df.groupby('CustomerId')['Amount'].sum())

if 'TransactionStartTime' in filtered_df.columns:
    st.subheader("Transactions dans le temps")
    df_time = filtered_df.groupby(filtered_df['TransactionStartTime'].dt.to_period('M')).size()
    st.line_chart(df_time)

if 'FraudResult' in filtered_df.columns:
    st.subheader("Transactions suspectes (FraudResult)")
    st.bar_chart(filtered_df['FraudResult'].value_counts())

if 'CustomerId' in filtered_df.columns and 'FraudResult' in filtered_df.columns:
    st.subheader("Top clients par nombre de fraudes")
    # On suppose que FraudResult == 1 indique une fraude
    fraud_count = filtered_df.groupby('CustomerId')['FraudResult'].sum()
    top_fraud_clients = fraud_count.sort_values(ascending=False).head(10)
    st.bar_chart(top_fraud_clients)

if 'ProductCategory' in filtered_df.columns and 'Amount' in filtered_df.columns and 'Value' in filtered_df.columns:
    st.subheader("Services les plus rentables (Amount vs Value)")
    # Calcul du profit par service
    filtered_df['Profit'] = filtered_df['Amount'] - filtered_df['Value']
    profit_by_service = filtered_df.groupby('ProductCategory')['Profit'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(profit_by_service)

if 'ChannelId' in filtered_df.columns:
    st.subheader("Répartition des transactions par canal")
    st.bar_chart(filtered_df['ChannelId'].value_counts())
