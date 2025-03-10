import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown("""
# Wildfire Incident Locations and Frequency

This section of the dashboard visualizes the **geographical distribution** and **frequency** of wildfires across California, focusing on **incident locations** and the **frequency of wildfires** by county. The data can be filtered by year to examine trends and patterns over time.

### Key Insights:
1. **Wildfire Frequency by County:**  
   The first chart is a **choropleth map** that visualizes the frequency of wildfires in each county, using color to indicate the number of incidents. This map highlights the counties most affected by wildfires, with darker colors representing less frequencies. By filtering the data by year, you can explore how wildfire occurrences have changed over time in different regions of California.

2. **Incident Locations Scaled by Area Burned:**  
   The second chart is a **scatter map** that shows the **locations of wildfire incidents** in California. The size of each point on the map represents the **area burned** (in acres). Hovering over the points will provide additional information, including the number of **homes destroyed**, **fatalities**, and **estimated financial losses** for each incident. This map allows us to see where the largest and most devastating wildfires have occurred across the state.

By filtering the data for different years, users can track wildfire patterns and better understand the areas that have faced the greatest damage. These maps are invaluable for policymakers, emergency responders, and anyone interested in the geographical impacts of wildfires in California.
""")

cal_fire = pd.read_csv('src/wildfire-dashboard/wildfire_dashboard/wildfire_proc.csv')

years_filter = st.slider("Select years", 2014, 2023, (2014, 2023))
years_filter_list = list(range(years_filter[0],years_filter[1]))
if years_filter[1]==years_filter[0]:
    st.write(f'Showing results for the year {years_filter[0]}')
else:    
    st.write(f'Showing results for years {years_filter[0]} - {years_filter[1]}')
cal_fire = cal_fire[cal_fire['year'].isin(years_filter_list)]

# Create DataFrame with California county names and FIPS codes
ca_counties = pd.DataFrame({
    "county": [
        "Alameda", "Alpine", "Amador", "Butte", "Calaveras", "Colusa", "Contra Costa", "Del Norte",
        "El Dorado", "Fresno", "Glenn", "Humboldt", "Imperial", "Inyo", "Kern", "Kings", "Lake",
        "Lassen", "Los Angeles", "Madera", "Marin", "Mariposa", "Mendocino", "Merced", "Modoc",
        "Mono", "Monterey", "Napa Valley", "Nevada", "Orange", "Placer", "Plumas", "Riverside",
        "Sacramento", "San Benito", "San Bernardino", "San Diego", "San Francisco", "San Joaquin",
        "San Luis Obispo", "San Mateo", "Santa Barbara", "Santa Clara", "Santa Cruz", "Shasta",
        "Sierra", "Siskiyou", "Solano", "Sonoma", "Stanislaus", "Sutter", "Tehama", "Trinity",
        "Tulare", "Tuolumne", "Ventura", "Yolo", "Yuba"
    ],
    "fips": [
        "06001", "06003", "06005", "06007", "06009", "06011", "06013", "06015", "06017", "06019",
        "06021", "06023", "06025", "06027", "06029", "06031", "06033", "06035", "06037", "06039",
        "06041", "06043", "06045", "06047", "06049", "06051", "06053", "06055", "06057", "06059",
        "06061", "06063", "06065", "06067", "06069", "06071", "06073", "06075", "06077", "06079",
        "06081", "06083", "06085", "06087", "06089", "06091", "06093", "06095", "06097", "06099",
        "06101", "06103", "06105", "06107", "06109", "06111", "06113", "06115"
    ]
})

cal_fire_fips = cal_fire.merge(ca_counties,on='county',how='left')

fips_freq = cal_fire_fips['fips'].value_counts().reset_index()

fips_freq = ca_counties.merge(fips_freq,on='fips',how='left').fillna(0)

# Create the choropleth map
fig = px.choropleth(
    fips_freq,
    geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
    locations='fips',
    color='count',
    color_continuous_scale="Viridis",
    scope="usa",
    labels={'count': 'Wildfire frequency'},
    hover_data={'county': True, 'fips': False}  # Show county name, hide FIPS
)

# Filter to show only California
fig.update_geos(
    fitbounds="locations",
    visible=False,
    lonaxis_range=[-125, -114], #Longitude range for california
    lataxis_range=[32, 42] #Latitude range for california
)

# Update layout
fig.update_layout(
    title='Wildfire frequency by county'
)

st.plotly_chart(fig)

#Scatter Map: Incident locations, scaled by area burned.

california_counties = {
    "Alameda": (37.6469, -121.8889),
    "Alpine": (38.5946, -119.8226),
    "Amador": (38.4493, -120.6561),
    "Butte": (39.6253, -121.5370),
    "Calaveras": (38.1960, -120.6800),
    "Colusa": (39.1789, -122.2376),
    "Contra Costa": (37.8534, -121.9018),
    "Del Norte": (41.7423, -123.8992),
    "El Dorado": (38.7426, -120.4358),
    "Fresno": (36.9859, -119.2321),
    "Glenn": (39.5913, -122.3933),
    "Humboldt": (40.7450, -123.8695),
    "Imperial": (33.0114, -115.4734),
    "Inyo": (36.5111, -117.4049),
    "Kern": (35.3431, -118.7270),
    "Kings": (36.0758, -119.8155),
    "Lake": (39.1014, -122.7539),
    "Lassen": (40.5882, -120.5889),
    "Los Angeles": (34.3203, -118.2251),
    "Madera": (37.2153, -119.7664),
    "Marin": (38.0717, -122.7214),
    "Mariposa": (37.5200, -119.8626),
    "Mendocino": (39.4363, -123.3911),
    "Merced": (37.1899, -120.7206),
    "Modoc": (41.5911, -120.7242),
    "Mono": (37.9375, -118.8876),
    "Monterey": (36.2070, -121.3542),
    "Napa Valley": (38.5073, -122.3323),
    "Nevada": (39.3284, -120.8136),
    "Orange": (33.7006, -117.7601),
    "Placer": (39.0916, -120.8039),
    "Plumas": (40.0033, -120.8398),
    "Riverside": (33.7436, -115.9936),
    "Sacramento": (38.4747, -121.3542),
    "San Benito": (36.6504, -121.0599),
    "San Bernardino": (34.8404, -116.1831),
    "San Diego": (32.8771, -116.7560),
    "San Francisco": (37.7400, -122.4467),
    "San Joaquin": (37.9176, -121.1710),
    "San Luis Obispo": (35.3793, -120.5433),
    "San Mateo": (37.4142, -122.2566),
    "Santa Barbara": (34.6206, -119.8205),
    "Santa Clara": (37.2259, -121.6989),
    "Santa Cruz": (37.0361, -122.0712),
    "Shasta": (40.7909, -122.1231),
    "Sierra": (39.5765, -120.5233),
    "Siskiyou": (41.5826, -122.5401),
    "Solano": (38.2567, -121.9358),
    "Sonoma": (38.5764, -122.9451),
    "Stanislaus": (37.6032, -120.9370),
    "Sutter": (39.0279, -121.6736),
    "Tehama": (40.0738, -122.2376),
    "Trinity": (40.6501, -123.1524),
    "Tulare": (36.2190, -118.8000),
    "Tuolumne": (38.0291, -119.9741),
    "Ventura": (34.3523, -119.1443),
    "Yolo": (38.7312, -121.9052),
    "Yuba": (39.2885, -121.3999)
}

scatter_df = cal_fire[["county",
                       "Area_Burned (Acres)",
                       "Homes_Destroyed",
                       "Fatalities",
                       "Estimated_Financial_Loss (Billion $)"
                      ]].groupby("county").sum().reset_index()

# Map county names to lat/lon
scatter_df["Latitude"] = scatter_df["county"].map(lambda x: california_counties.get(x, (None, None))[0])
scatter_df["Longitude"] = scatter_df["county"].map(lambda x: california_counties.get(x, (None, None))[1])

fig = px.scatter_mapbox(
    scatter_df,
    lat="Latitude",
    lon="Longitude",
    size="Area_Burned (Acres)",  # Scale points by area burned
    hover_name="county",
    hover_data={
        "Area_Burned (Acres)": True,
        "Latitude": False,
        "Longitude": False,
        "Homes_Destroyed": True,
        "Fatalities": True,
        "Estimated_Financial_Loss (Billion $)": True
    },
    zoom=4,  # Lower zoom for full-state view
    center={"lat": 37.5, "lon": -119.5},  # Centered over California
    mapbox_style="carto-positron"
)

# Update layout
fig.update_layout(
    title='Incident locations, scaled by area burned'
)
st.plotly_chart(fig)