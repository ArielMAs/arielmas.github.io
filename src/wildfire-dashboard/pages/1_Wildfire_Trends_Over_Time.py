import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown("""
# How have wildfires changed over time?

Explore the trends and changes in wildfire incidents across California, focusing on **frequency**, **seasonality**, and **area burned** over the past decade.

### Key Insights:
1. **Monthly and Yearly Frequency of Wildfires:**  
   The first chart is a **heatmap** showing the frequency of wildfires on a **month-by-year** basis. This heatmap reveals seasonal trends, highlighting months with the highest number of incidents each year. The month-by-month comparison is essential for understanding the seasonal nature of wildfires in California, as well as how this has evolved over time.

2. **Number of Wildfires per Year/Month:**  
   The second chart is a **line chart** that visualizes the total number of wildfires per year or month (depending on the user's selection). This graph shows overall wildfire trends, allowing us to see if the frequency of wildfires is increasing, decreasing, or remaining stable across the years or months.

3. **Area Burned (Acres) per Year/Month:**  
   The final chart is a **bar chart** that illustrates the **area burned** in acres per year or month. This chart helps to compare how the scale of the wildfires has changed over time, which could indicate larger or more intense fires as the years progress. By selecting the appropriate time period, users can track how the severity of the wildfires has evolved.

### Filters:
- **Location Filter:** Select a specific **county** in California or view data for **all counties**.
- **Cause Filter:** Filter the data by the **cause of the wildfire** (e.g., lightning, human activity).
- **Time Period Filter:** Toggle between viewing data by **year** or **month** for frequency and area burned.

This dashboard helps to track **wildfire trends** over time, providing a clearer picture of how wildfires are changing, their seasonal patterns, and the extent of their damage. It’s a powerful tool for understanding the broader implications of these incidents and for informing policy decisions and preparedness strategies.
""")


cal_fire = pd.read_csv('wildfire_proc.csv')

st.title("How have wildfires changed over time?")
st.markdown("""
            * Explore trends in wildfire frequency over the past decade.
            * Toggle between yearly and monthly trends.
            """)

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


#Heatmap: Month-wise frequency of wildfires (seasonal trends).
cal_fire_month_year = cal_fire[['Incident_ID','year','month']]

# Count incidents per Year-Month
incident_counts = cal_fire_month_year.groupby(["year", "month"]).size().reset_index(name="Count")

# Pivot the data for the heatmap (Years as rows, Months as columns)
heatmap_data = incident_counts.pivot(index="year", columns="month", values="Count").fillna(0)

months_of_year_list = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
years_list = list(range(2014,2024))
heatmap_data = heatmap_data.reindex(index=years_list, columns=months_of_year_list, fill_value=0)

fig = px.imshow(heatmap_data,text_auto=True,
                labels=dict(x="Month", y="Year", color="Number of wildfires"),
                x=['Jan', 'Feb', 'Mar', 'Apr', 'May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
                y=['2014', '2015','2016','2017','2018','2019','2020','2021','2022','2023'],
                title='Incident Counts by Month and Year'
               )

st.plotly_chart(fig)


#Line chart Number of incidents per year (2014–2024).
pick_year_month = st.selectbox('Pick to see Monthly/Yearly trend over time',('Month','Year'))
if pick_year_month == 'Year':
    metric = 'year'
elif pick_year_month == 'Month':
    metric = 'month'

month_freq = cal_fire[metric].value_counts().sort_index().reset_index()
fig = px.line(month_freq, x=metric, y="count", title=f'Number of wildfires per {metric}' )
fig.update_layout(
    xaxis_title=pick_year_month,
    yaxis_title="Number of wildfires"
)
st.plotly_chart(fig)

#Bar Chart: Area burned per year (in acres).
cal_fire_year_area_burned = cal_fire[[metric,'Area_Burned (Acres)']]

# Count incidents per Year-Month
area_burned_per_year = cal_fire_year_area_burned.groupby(metric).sum().reset_index()

fig = px.bar(area_burned_per_year, y='Area_Burned (Acres)', x=metric, text_auto='.2s',
            title=f"Area Burned (Acres) per {metric}")
fig.update_layout(
    xaxis_title=pick_year_month,
    yaxis_title="Area Burned (Acres)"
)
fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
st.plotly_chart(fig)