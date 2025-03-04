#🏠 1️⃣ Home Page (Introduction & Key Metrics)
#📍 Purpose:

#Provide an overview of California wildfires (2014-2024).
#Summarize total incidents, area burned, financial losses, and human impact.
#📊 Elements:
#✅ Title: "California Wildfire Dashboard (2014-2024)"
#✅ Subtitle: "Explore trends, financial losses, and human impact of wildfires in California."
#✅ Key Metrics (Displayed at the Top):

#Total Incidents
#Total Area Burned (Acres)
#Total Financial Loss ($M)
#Total Fatalities & Injuries
#✅ Navigation Instructions: Explain that users can select pages to explore specific wildfire trends.

import streamlit as st
import pandas as pd


st.sidebar.write("Users can select pages to explore specific wildfire trends.")

cal_fire = pd.read_csv('California_Wildfire_Damage.csv')

totalAreaBurned = cal_fire['Area_Burned (Acres)'].sum()
totalFinancialLoss = cal_fire['Estimated_Financial_Loss (Million $)'].sum()
totalFatalities = cal_fire['Fatalities'].sum()
totalInjuries = cal_fire['Injuries'].sum()
numberOfWildfires = len(cal_fire)


# Markdown Content
st.markdown("""
    # Welcome to the California Wildfire Dashboard
    This dashboard provides an interactive way to explore trends, financial losses, and the human impact of wildfires in California from 2014 to 2024. 
    You can use the sidebar to navigate through different pages for detailed insights on specific wildfire-related trends. The source data can be found at [kaggle](https://www.kaggle.com/datasets/vivekattri/california-wildfire-damage-2014-feb2025).

    ## Key Insights:
    * **Total Area Burned (Acres):** The total area burned by wildfires in California over the past decade.
    * **Total Financial Loss ($ Million):** The financial impact of these wildfires on California.
    * **Total Fatalities and Injuries:** The tragic human toll resulting from these incidents.
    
    The following key metrics summarize the overall wildfire impact in California over the past decade:
""", unsafe_allow_html=True)

first_c,second_c,third_c = st.columns(3)
first_c.metric("Total Area Burned (Acres)",totalAreaBurned)
second_c.metric("Total Financial Loss ($M)",totalFinancialLoss)
third_c.metric("Total number of wildfires",numberOfWildfires)
first_c.metric("Total Fatalities",totalFatalities)
third_c.metric("Total Injuries",totalInjuries)

