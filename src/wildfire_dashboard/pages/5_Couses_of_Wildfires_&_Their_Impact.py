#(E) Causes of Wildfires & Their Impact
#Goal: Determine how wildfire causes affect severity.
#🔹 Visualizations:

#Pie Chart: Percentage of wildfires by cause (Lightning, Human Activity, Unknown).
#Box Plot: Area burned by wildfire cause (which causes the most damage?).
#Bar Chart: Financial losses by cause type.
#Insights to extract:
#📌 Do human-caused wildfires lead to more damage than natural ones?
#📌 How does each cause affect financial losses and injuries?
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

st.markdown("""
# Wildfire Causes, Area Burned, and Financial Losses

This section of the dashboard provides insights into various factors that contribute to wildfires in California, including their causes, the area burned, and the financial losses associated with them. The data presented is filtered based on the years selected (2014–2023) and, if applicable, the location of the wildfires.

### Key Insights:
1. **Percentage of Wildfires by Cause (Lightning, Human Activity, Unknown):**  
   The first chart presents a **pie chart** that shows the percentage of wildfires caused by different factors. The causes are categorized into three main types: **Lightning**, **Human Activity**, and **Unknown**. This breakdown helps us understand the relative contributions of each cause to the overall wildfire occurrence in California.

2. **Area Burned by Wildfire Cause:**  
   The second chart, a **box plot**, visualizes the area burned by wildfires categorized by cause. By looking at the distribution of the **area burned** for each cause type, we can gain insights into which types of wildfires tend to cause the most damage. This information can help in planning fire management strategies and prioritizing resources.

3. **Financial Losses by Wildfire Cause:**  
   The final chart presents a **bar chart** that displays the **estimated financial losses** incurred by each wildfire cause. The chart helps to quantify the economic impact of wildfires in California, with significant losses resulting from both human activity and natural causes like lightning. This information is valuable for understanding the financial burden of wildfires and can guide future prevention and mitigation strategies.

By filtering the data based on the years and location, users can explore how the causes and impacts of wildfires change over time and across different regions.
""")

cal_fire = pd.read_csv('wildfire_proc.csv')

counties = list(cal_fire['county'].unique())
counties.insert(0,'All')


counties_filter = st.selectbox(
    "Select Location",
    counties
)


years_filter = st.slider("Select years", 2014, 2023, (2014, 2023))
years_filter_list = list(range(years_filter[0],years_filter[1]))

cal_fire = cal_fire[cal_fire['year'].isin(years_filter_list)]

if counties_filter!='All':
    cal_fire = cal_fire[cal_fire['county']==counties_filter]


#Pie Chart: Percentage of wildfires by cause (Lightning, Human Activity, Unknown).
fire_cause = cal_fire['Cause'].value_counts().reset_index()
fire_cause['p'] = fire_cause['count']/fire_cause['count'].sum()

fig = px.pie(fire_cause, values='p', names='Cause', title='Pie Chart: Percentage of wildfires by cause (Lightning, Human Activity, Unknown)')
st.plotly_chart(fig)

#Box Plot: Area burned by wildfire cause (which causes the most damage?).
fig = px.box(cal_fire, x="Cause", y="Area_Burned (Acres)")
fig.update_layout(
    title='Area burned by wildfire cause',
    xaxis_title='Wildfire Cause',
    yaxis_title='Area Burned (Acres)'
    )
st.plotly_chart(fig)

#Bar Chart: Financial losses by cause type.
loss_couse = cal_fire[['Cause','Estimated_Financial_Loss (Million $)']].groupby('Cause',as_index=False).sum()
fig = px.bar(loss_couse, x='Cause', y='Estimated_Financial_Loss (Million $)')
fig.update_layout(
    title='Financial losses by cause type',
    xaxis_title='Wildfire Cause',
    yaxis_title='Estimated Financial_Loss (Million $)'
    )

st.plotly_chart(fig)