import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns

st.markdown("""
# Financial Impact of Wildfires: Damages and Losses

This section of the dashboard provides a detailed look at the **financial impact** of wildfires in California, focusing on damages to homes, businesses, and vehicles, as well as the overall **estimated financial losses**. The data is filtered based on location, allowing for a closer examination of how different regions are affected by these catastrophic events.

### Key Insights:
1. **Comparison of Damages to Homes, Businesses, and Vehicles per Year:**  
   The first chart is a **stacked bar chart** that compares the number of **homes destroyed**, **businesses destroyed**, and **vehicles damaged** each year from 2014 to 2023. This allows us to see how these damages have evolved over time, providing insights into the trends and the varying severity of wildfire impacts on different sectors of society. The grouped bars make it easy to compare the damage across these categories for each year.

2. **Distribution of Estimated Financial Losses per Wildfire:**  
   The second chart is a **histogram** that shows the distribution of **estimated financial losses** due to wildfires, represented in millions of dollars. The **kernel density estimate (KDE)** overlay helps to visualize the distribution of financial losses across the wildfires in the dataset. This chart helps us understand the frequency of various levels of financial loss and highlights any particularly high-loss incidents, providing a sense of the economic burden wildfires impose on the state.

By filtering the data based on the selected location, users can gain insights into the financial consequences of wildfires at both the local and state levels, providing valuable information for future planning and mitigation strategies.
""")

cal_fire = pd.read_csv('wildfire_proc.csv')

counties = list(cal_fire['county'].unique())
counties.insert(0,'All')

counties_filter = st.selectbox(
    "Select Location",
    counties
)

if counties_filter!='All':
    cal_fire = cal_fire[cal_fire['county']==counties_filter]

#Stacked Bar Chart: Comparison of homes, businesses, and vehicles damaged per year.
finance_by_year = cal_fire[['year',
                            'Homes_Destroyed',
                            'Businesses_Destroyed',
                            'Vehicles_Damaged']].groupby('year').sum().reset_index()
finance_vars = ['Homes_Destroyed','Businesses_Destroyed','Vehicles_Damaged']

# Create figure
fig = go.Figure()

# Add traces
fig.add_trace(go.Bar(x=finance_by_year['year'], y=finance_by_year['Homes_Destroyed'], name='Homes_Destroyed'))
fig.add_trace(go.Bar(x=finance_by_year['year'], y=finance_by_year['Businesses_Destroyed'], name='Businesses_Destroyed'))
fig.add_trace(go.Bar(x=finance_by_year['year'], y=finance_by_year['Vehicles_Damaged'], name='Vehicles_Damaged'))
# Update layout
fig.update_layout(
    barmode='group',  # Grouped bars
    title='Grouped Bar Chart',
    xaxis_title='Year',
    yaxis_title='Values',
    xaxis=dict(tickmode='linear')
)

# Show figure
st.plotly_chart(fig)

fig = plt.figure(figsize=(10, 4))
sns.histplot(cal_fire['Estimated_Financial_Loss (Million $)'], bins=30, kde=True, color='skyblue', edgecolor='black')

plt.title('Estimated Financial Loss (Million $) distribution')
plt.xlabel('Estimated Financial Loss (Million $)')
plt.ylabel('Frequency')
st.pyplot(fig)

