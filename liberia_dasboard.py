import streamlit as st
import pandas as pd
import plotly.express as px
from pandas_datareader import wb

# Cache data to improve performance
@st.cache_data
def load_data():
    # Get data specifically for Liberia
    df = wb.download(indicator='SP.POP.TOTL', country='LBR', start=1960, end=2023)
    df = df.reset_index()
    df = df.rename(columns={'SP.POP.TOTL': 'Population', 'country': 'Country Code'})
    df['Country'] = 'Liberia'
    df = df.melt(id_vars=['Country', 'Country Code'], 
                var_name='Year', 
                value_name='Population')
    df['Year'] = df['Year'].astype(int)
    return df.dropna()

# Load the data
population_df = load_data()

# Dashboard Title
st.title("🇱🇷 Liberia Population Dashboard")

# Calculate latest year metrics
latest_year = population_df['Year'].max()
previous_year = latest_year - 1

# Main metrics
current_pop = population_df[population_df['Year'] == latest_year]['Population'].values[0]
previous_pop = population_df[population_df['Year'] == previous_year]['Population'].values[0]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(f"Current Population ({latest_year})", f"{current_pop/1e6:.2f}M")

with col2:
    growth = current_pop - previous_pop
    st.metric("Annual Growth", f"{growth/1e3:.1f}K")

with col3:
    growth_rate = ((current_pop - previous_pop)/previous_pop) * 100
    st.metric("Growth Rate", f"{growth_rate:.2f}%")

# Population trends over time
st.subheader("Population Trend (1960-Present)")
fig = px.line(
    population_df,
    x="Year",
    y="Population",
    title="Liberia's Population Growth",
    markers=True
)
st.plotly_chart(fig, use_container_width=True)

# Population distribution by decade
st.subheader("Population by Decade")
population_df['Decade'] = (population_df['Year'] // 10) * 10
fig2 = px.bar(
    population_df.groupby('Decade').last().reset_index(),
    x="Decade",
    y="Population",
    title="Population Growth by Decade"
)
st.plotly_chart(fig2, use_container_width=True)

# Demographic highlights
st.subheader("Key Statistics")
latest_data = population_df[population_df['Year'] == latest_year].iloc[0]
st.markdown(f"""
- Liberia represents {latest_data.Population/8e9:.4f}% of world population
- Population density: {latest_data.Population/111369:.1f} people/km²
- Annual growth equivalent: {growth/365:.0f} people/day
""")

# Data table
st.subheader("Historical Data")
st.dataframe(population_df[['Year', 'Population']], use_container_width=True)