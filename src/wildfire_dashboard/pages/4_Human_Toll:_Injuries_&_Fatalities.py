
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

# Display Markdown and text
st.markdown("""
# Human Toll: Injuries & Fatalities

This section of the dashboard provides an in-depth look into the human toll caused by wildfires in California, focusing on two key metrics: **Injuries** and **Fatalities**. The data presented is derived from wildfire incidents between 2014 and 2024, highlighting how the frequency of injuries and fatalities varies by year and wildfire size.

### Key Insights:
1. **Trends Over Time (2014–2024):**  
   The first chart visualizes the **number of injuries** and **fatalities** reported each year, helping us understand how the severity of wildfires has evolved in terms of human impact. The chart allows us to see how the frequency of these incidents changes over time, potentially indicating the effectiveness of wildfire management strategies or the increasing intensity of wildfires in recent years.

2. **Impact of Wildfire Size on Casualties:**  
   The second chart breaks down **injuries and fatalities** by the size of the wildfire, categorized into three groups: Small, Medium, and Large. This comparison offers valuable insights into how the scale of a wildfire influences the human toll. Larger wildfires tend to cause more injuries and fatalities, but even smaller fires can still have significant impacts on communities.

By filtering the data based on location and wildfire cause, users can tailor the analysis to specific regions or factors, providing a deeper understanding of the human consequences of wildfires in California.
""")

cal_fire = pd.read_csv('wildfire_proc.csv')

counties = list(cal_fire['county'].unique())
counties.insert(0,'All')
causes = list(cal_fire['Cause'].unique())
causes.insert(0,'All')

counties_filter = st.selectbox(
    "Select Location",
    counties
)

cause_filter = st.selectbox(
    "Select Wildfire Cause",
    causes
)

if cause_filter!='All':
    cal_fire = cal_fire[cal_fire['Cause']==cause_filter]

if counties_filter!='All':
    cal_fire = cal_fire[cal_fire['county']==counties_filter]



#Line chart Sum of Injuries and Fatalities per year (2014–2024).
year_injury_fatalities = cal_fire[['year','Injuries','Fatalities']].groupby('year').sum().sort_index()

def line_chart_plot(data,col):
    # Create the line chart
    plt.plot(data.index, data[col], marker='o')
    
    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Frequency')
    plt.title(f'Number of {col} per year (2014–2024)')
    
    # Display the chart
    plt.show()

# Create figure
fig = go.Figure()
fig.add_trace(go.Line(x=year_injury_fatalities.index, y=year_injury_fatalities['Injuries'], name='Injuries'))
fig.add_trace(go.Line(x=year_injury_fatalities.index, y=year_injury_fatalities['Fatalities'], name='Fatalities'))
# Update layout to add title and axis labels
fig.update_layout(
    title="Number of Injuries/Fatalities per year (2014–2024)",
    xaxis_title="X-axis Label",
    yaxis_title="Y-axis Label"
)

st.plotly_chart(fig)

#Bar Chart: Fatalities and injuries by wildfire size.
conditions = [
    cal_fire['Area_Burned (Acres)']<15916,
    (cal_fire['Area_Burned (Acres)']>=15916) & 
    (cal_fire['Area_Burned (Acres)']<39775),
    (cal_fire['Area_Burned (Acres)']>=39775)
]
choices = [
    'Small',
    'Medium',
    'Large'
]
cal_fire['Area_Burned_cat'] = np.select(conditions, choices, default='unknown')
burned_cat_fatel_inj = cal_fire[['Area_Burned_cat','Injuries','Fatalities']].groupby('Area_Burned_cat').sum()

cat_order = ['Small','Medium','Large']
# Convert the index to a categorical type with the custom order
burned_cat_fatel_inj.index = pd.Categorical(burned_cat_fatel_inj.index, categories=cat_order, ordered=True)

# Sort the DataFrame by the index
burned_cat_fatel_inj_sorted = burned_cat_fatel_inj.sort_index()

# Create figure
fig = go.Figure()

# Add traces
fig.add_trace(go.Bar(x=burned_cat_fatel_inj_sorted.index, y=burned_cat_fatel_inj_sorted['Injuries'], name='Injuries'))
fig.add_trace(go.Bar(x=burned_cat_fatel_inj_sorted.index, y=burned_cat_fatel_inj_sorted['Fatalities'], name='Fatalities'))
# Update layout
fig.update_layout(
    barmode='group',  # Grouped bars
    title='Fatalities and injuries by wildfire size',
    xaxis_title='Wildfire size',
    yaxis_title='Frequency',
    xaxis=dict(tickmode='linear')
)

# Show figure
st.plotly_chart(fig)
