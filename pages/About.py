import streamlit as st
import plotly.express as px
import pandas as pd
import os
import pycountry
import json

st.set_page_config(page_title="About - Where Should I Live?", page_icon="🌍", layout="wide")

# Function to get real countries data from our dataset
def get_countries_data():
    # Load the real dataset
    try:
        df = pd.read_csv("final_merged_dataset_with_knn.csv")
        
        # Clean up the data
        # The first column seems to be country names but has no header - rename it
        df = df.rename(columns={df.columns[0]: "country"})
        
        # Add ISO code for mapping
        countries_with_iso = []
        
        # Dictionary for country name mapping to ISO
        name_to_iso = {
            'united states': 'USA', 'united kingdom': 'GBR', 'russia': 'RUS',
            'south korea': 'KOR', 'congo': 'COD',  # Assuming this is Democratic Republic of Congo
            'ivory coast': 'CIV', 'myanmar': 'MMR', 'taiwan': 'TWN',
            'bosnia & herzegovina': 'BIH', 'north macedonia': 'MKD',
            'trinidad & tobago': 'TTO', 'hong kong': 'HKG', 'turkey': 'TUR'
        }
        
        for country_name in df['country']:
            try:
                # Try direct lookup first
                if country_name in name_to_iso:
                    iso = name_to_iso[country_name]
                else:
                    # Otherwise try pycountry
                    country = pycountry.countries.search_fuzzy(country_name)[0]
                    iso = country.alpha_3
                
                countries_with_iso.append({
                    "country": country_name.title(),
                    "iso_alpha_3": iso,
                    "has_data": True
                })
            except (LookupError, IndexError):
                # If country not found, still add it but mark the ISO as unknown
                print(f"Could not find ISO code for {country_name}")  # Use print instead of st.warning
                countries_with_iso.append({
                    "country": country_name.title(),
                    "iso_alpha_3": "Unknown",
                    "has_data": False
                })
        
        # Create a dataframe with ISO codes
        countries_df = pd.DataFrame(countries_with_iso)
        
        # Filter out any duplicate countries
        countries_df = countries_df.drop_duplicates(subset=['country'])
        
        # Only keep rows with valid ISO codes
        countries_df = countries_df[countries_df['iso_alpha_3'] != "Unknown"]
        
        return countries_df
        
    except Exception as e:
        st.error(f"Error loading country data: {e}")
        
        # Fallback to empty dataframe
        return pd.DataFrame(columns=["country", "iso_alpha_3", "has_data"])

# Page title
st.title("About 'Where Should I Live?'")

# Project Description
st.markdown("""
## 🌎 Project Overview

**'Where Should I Live?'** is a personalized recommendation engine designed to help you find your dream country based on your preferences. 

Created by students of the Le Wagon Data Science & AI bootcamp, this project was born from a simple question: with so many amazing places in the world, how do you find the perfect match for your lifestyle?

## 🔍 What We Do

We analyze your preferences across several key factors:
- 🌡️ Climate preferences
- 💰 Cost of living considerations
- 🏥 Healthcare quality
- 🛡️ Safety metrics
- 🌐 Internet connectivity

Then we match you with countries that best fit your unique requirements, using real-world data from reliable sources.

## 📊 Our Data

Our database includes comprehensive information on **151 countries** worldwide, covering all developed nations and many more. All recommendations are based on actual data, not opinions or stereotypes.
""")

# Interactive Map
st.markdown("## 🗺️ Countries in Our Database")

countries_df = get_countries_data()

# Create the Choropleth map with Plotly
if not countries_df.empty:
    fig = px.choropleth(
        countries_df,
        locations="iso_alpha_3",
        color="has_data",
        hover_name="country",
        color_discrete_map={True: "green", False: "lightgray"},
        labels={"has_data": "Included in Database"},
        title=f"Countries Included in Our Database ({len(countries_df)} total)"
    )
    
    fig.update_layout(
        coloraxis_showscale=False,  # No need for legend since all countries are included
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Could not generate map - no country data available")

# Additional Info
st.markdown("""
## 👥 Creators

This project was created by students of the Le Wagon Data Science & AI bootcamp batch #1835 who wanted to build something useful that combines data science with a real-world application.


""")

# Footer
st.markdown("---")
st.markdown("© 2025 Where Should I Live") 