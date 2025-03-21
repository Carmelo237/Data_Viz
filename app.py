import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement des données avec mise en cache
@st.cache_data
def load_data():
    return pd.read_csv(r"C:\\Users\\brice\\OneDrive\\Bureau\\HETIC\\Data Viz\\projet\\Financials_cleaned.csv")

df_cleaned = load_data()

# Appliquer un style sombre global
st.markdown(
    """
    <style>
        body {
            background-color: #1e1e1e;
            color: white;
        }
        .kpi-card {
            background: #2b2b2b;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.2);
            margin: 10px;
        }
        .kpi-value {
            font-size: 24px;
            font-weight: bold;
            color: #ffcc00;
        }
        .sidebar .stSelectbox {
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Ajout d'un sélecteur pour filtrer les données
country_filter = st.sidebar.selectbox("🌍 Sélectionnez un pays", ["Tous"] + list(df_cleaned["Country"].unique()))
if country_filter != "Tous":
    df_cleaned = df_cleaned[df_cleaned["Country"] == country_filter]

year_filter = st.sidebar.selectbox("📆 Sélectionnez une année", ["Toutes"] + sorted(df_cleaned["Year"].unique()))
if year_filter != "Toutes":
    df_cleaned = df_cleaned[df_cleaned["Year"] == year_filter]

# Calcul des KPIs
total_sales = df_cleaned["Sales"].sum()
total_units_sold = df_cleaned["Units Sold"].sum()
total_profit = df_cleaned["Profit"].sum()
avg_sale_price = df_cleaned["Sale Price"].mean()
avg_manufacturing_price = df_cleaned["Manufacturing Price"].mean()
profit_margin = (total_profit / total_sales) * 100 if total_sales else 0

# Affichage des KPIs sous forme de cartes bien espacées
st.title("📊 Tableau de Bord des Ventes")

st.markdown("### **📌 Indicateurs Clés de Performance (KPI)**")

kpi_cols = st.columns(3)

kpi_data = [
    ("💰 Ventes Totales", f"{total_sales:,.0f} €"),
    ("📦 Total Unités Vendues", f"{total_units_sold:,.0f}"),
    ("💵 Profit Total", f"{total_profit:,.0f} €"),
    ("💲 Prix de Vente Moyen", f"{avg_sale_price:.2f} €"),
    ("🏠 Prix de Fabrication Moyen", f"{avg_manufacturing_price:.2f} €"),
    ("📈 Marge Bénéficiaire", f"{profit_margin:.2f} %"),
]

for i, (label, value) in enumerate(kpi_data):
    with kpi_cols[i % 3]:
        st.markdown(
            f"""
            <div class="kpi-card">
                <h4>{label}</h4>
                <p class="kpi-value">{value}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Affichage des 10 premières lignes du dataset
st.subheader("👀 Aperçu des 10 premières lignes des données")
st.dataframe(df_cleaned.head(10))

# Classement des pays par ventes et profits
top_countries_sales = df_cleaned.groupby("Country")["Sales"].sum().nlargest(10).reset_index()
top_countries_profit = df_cleaned.groupby("Country")["Profit"].sum().nlargest(10).reset_index()

st.subheader("🏆 Pays par Ventes")
fig_countries_sales = px.bar(
    top_countries_sales, x="Sales", y="Country", orientation='h',
    title="Top 10 Pays par Ventes", text_auto=True, color="Sales", color_continuous_scale="Blues"
)
st.plotly_chart(fig_countries_sales, use_container_width=True)

st.subheader("💰 Pays par Profits")
fig_countries_profit = px.bar(
    top_countries_profit, x="Profit", y="Country", orientation='h',
    title="Top 10 Pays par Profits", text_auto=True, color="Profit", color_continuous_scale="Greens"
)
st.plotly_chart(fig_countries_profit, use_container_width=True)


# Ajout d'un graphique des ventes cumulées
st.subheader("📈 Évolution des Ventes Cumulées")
sales_per_month = df_cleaned.groupby("Month Name")["Sales"].sum().reset_index()
sales_per_month["Cumulative Sales"] = sales_per_month["Sales"].cumsum()
fig_cumulative_sales = px.line(
    sales_per_month, x="Month Name", y="Cumulative Sales", title="Ventes Cumulées Mensuelles",
    markers=True, line_shape='spline', color_discrete_sequence=["#FF5733"]
)
st.plotly_chart(fig_cumulative_sales, use_container_width=True)

# Ajout d'un histogramme pour COGS vs Produits
st.subheader("📉 COGS vs Produits")
cogs_per_product = df_cleaned.groupby("Product")["COGS"].sum().reset_index().sort_values("COGS")
fig_cogs = px.bar(
    cogs_per_product, x="COGS", y="Product", orientation='h',
    title="COGS par Produit (Ordre Croissant)", text_auto=True, color="COGS", color_continuous_scale="Reds"
)
st.plotly_chart(fig_cogs, use_container_width=True)

# Histogramme des profits par segment
st.subheader("💹 Profits par Segment")
profits_per_segment = df_cleaned.groupby("Segment")["Profit"].sum().reset_index().sort_values("Profit")
fig_segment_profit = px.bar(
    profits_per_segment, x="Profit", y="Segment", orientation='h',
    title="Profits par Segment (Ordre Croissant)", text_auto=True, color="Profit", color_continuous_scale="Blues"
)
st.plotly_chart(fig_segment_profit, use_container_width=True)
