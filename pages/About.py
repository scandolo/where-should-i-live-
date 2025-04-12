import streamlit as st
import plotly.express as px
import pandas as pd
import os
import pycountry

st.set_page_config(page_title="Where Should I Live?", page_icon="🌍",
                   #layout="wide"
                   )

# Function to get countries data from the real dataset
def get_countries_data():
    # Path to the real dataset
    real_dataset = "final_merged_dataset_with_knn.csv"
    
    if os.path.exists(real_dataset):
        # Load the real dataset
        df = pd.read_csv(real_dataset)
        
        # Extract country names (first column, index=0)
        countries = df.iloc[:, 0].tolist()
        
        # Create a mapping dictionary for country names to ISO codes
        iso_map = {}
        for country in pycountry.countries:
            iso_map[country.name.lower()] = country.alpha_3
            # Add some common variations
            if country.name.lower() == "united states of america":
                iso_map["united states"] = country.alpha_3
            elif country.name.lower() == "united kingdom":
                iso_map["uk"] = country.alpha_3
            elif country.name.lower() == "russian federation":
                iso_map["russia"] = country.alpha_3
            
        # Function to get ISO code for a country name
        def get_iso_code(country_name):
            # Try to get the code directly
            country_name = country_name.lower()
            if country_name in iso_map:
                return iso_map[country_name]
            
            # Try to find the closest match
            for name, code in iso_map.items():
                if country_name in name or name in country_name:
                    return code
            
            # Some manual mappings for special cases
            special_cases = {
                "congo": "COG",
                "ivory coast": "CIV",
                "czech republic": "CZE",
                "united kingdom": "GBR",
                "united states": "USA",
                "russia": "RUS",
                "south korea": "KOR",
                "north korea": "PRK"
            }
            
            if country_name in special_cases:
                return special_cases[country_name]
                
            # If no match is found
            print(f"No ISO code found for: {country_name}")
            return None
        
        # Map country names to ISO codes
        iso_codes = [get_iso_code(country) for country in countries]
        
        # Create a new dataframe with the country names and ISO codes
        countries_df = pd.DataFrame({
            'country': countries,
            'iso_alpha_3': iso_codes
        })
        
        # Remove rows with None in iso_alpha_3
        countries_df = countries_df.dropna(subset=['iso_alpha_3'])
        
        return countries_df
    else:
        st.error(f"Dataset file '{real_dataset}' not found. Please check the file path.")
        # Return empty dataframe if file not found
        return pd.DataFrame(columns=['country', 'iso_alpha_3'])

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

Our database includes comprehensive information on **155 countries** worldwide, covering all developed nations and many more. All recommendations are based on actual data, not opinions or stereotypes.
""")

# Interactive Map
st.markdown("## 🗺️ Countries in Our Database")

# Get the real country data
countries_df = get_countries_data()

# Create the Choropleth map with Plotly
fig = px.choropleth(
    countries_df,
    locations="iso_alpha_3",
    color_discrete_sequence=["green"],
    hover_name="country",
    title="Countries Included in Our Database"
)

fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='natural earth'
    )
)

st.plotly_chart(fig, use_container_width=True)

# Display country count
st.info(f"Our dataset includes {len(countries_df)} countries from around the world.")

# Additional Info
st.markdown("""
## 👥 The Team

This project was created by students of the Le Wagon Data Science & AI bootcamp who wanted to build something useful that combines data science with real-world application.

## 🛠️ Technology

- **Backend**: Python-based recommendation algorithm with data analysis
- **Frontend**: Streamlit interactive web interface
- **Data Sources**: Multiple reliable international databases on cost of living, climate, healthcare, safety, and internet infrastructure
""")

# Footer
st.markdown("---")
st.markdown("© 2023 Where Should I Live") 