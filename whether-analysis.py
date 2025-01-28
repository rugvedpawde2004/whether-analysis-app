import streamlit as st
import pandas as pd

import seaborn as sns
import plotly.express as px

# Load the dataset
try:
    weather_data = pd.read_csv('pune_weather_with_regions.csv')
except FileNotFoundError:
    st.error("Error: pune_weather_with_regions.csv not found. Please upload the file.")
    st.stop()  # Stop execution if file not found

# Data preprocessing
weather_data['date'] = pd.to_datetime(weather_data['date'], format='%d-%m-%Y', errors='coerce') # Handle potential date parsing errors
weather_data = weather_data.dropna(subset=['date']) #Drop rows with invalid dates
weather_data['month'] = weather_data['date'].dt.to_period('M')

# Monthly Aggregation
monthly_aggregated_data = weather_data.groupby('month').agg({
    'Temperature': 'mean',
    'Humidity': 'mean',
    'Rainfall': 'mean'
}).reset_index()

monthly_aggregated_data['month'] = monthly_aggregated_data['month'].dt.to_timestamp()

# --- Streamlit App ---
st.title("Pune Weather Analysis")

# Display the raw data (optional)
if st.checkbox("Show Raw Data"):
    st.write(weather_data)

# Monthly Aggregated Data
st.subheader("Monthly Aggregated Data")
st.write(monthly_aggregated_data)


# --- Plots ---
import matplotlib.pyplot as plt
st.subheader("Temperature Trends Over Time")
fig_temp = plt.figure(figsize=(10, 6))  # Adjusted figure size for Streamlit
plt.plot(monthly_aggregated_data['month'], monthly_aggregated_data['Temperature'], marker='*', color='blue', label='Temperature (°C)')
plt.title('Temperature Trends Over Time')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.grid(alpha=0.5)
plt.legend()
st.pyplot(fig_temp)  # Use st.pyplot to display Matplotlib plots


st.subheader("Rainfall Trends Over Time")
fig_rain = plt.figure(figsize=(10, 6))
plt.plot(monthly_aggregated_data['month'], monthly_aggregated_data['Rainfall'], marker='>', color='red', label='Rainfall (mm)')
plt.title('Rainfall Trends Over Time')
plt.xlabel('Date')
plt.ylabel('Rainfall (mm)')
plt.grid(alpha=0.5)
plt.legend()
st.pyplot(fig_rain)

st.subheader("Average Monthly Rainfall (Bar Chart)")
fig_rain_bar = plt.figure(figsize=(10, 6))
sns.barplot(x=monthly_aggregated_data['month'].dt.month, y=monthly_aggregated_data['Rainfall'], palette="Blues_d")
plt.title('Average Monthly Rainfall')
plt.xlabel('Month')
plt.ylabel('Rainfall (mm)')
plt.grid(axis='y', alpha=0.3)
st.pyplot(fig_rain_bar)

st.subheader("Temperature Trends Across Regions (FacetGrid)")
g = sns.FacetGrid(weather_data, col='Region', col_wrap=3, height=4, sharey=True)
g.map(sns.lineplot, 'date', 'Temperature')
g.set_titles('{col_name}')
g.set_axis_labels('Date', 'Temperature')
st.pyplot(g.fig) # Access the figure from the FacetGrid and display it


st.subheader("Scatter Plot of Rainfall vs. Temperature")
fig_scatter = plt.figure(figsize=(10, 6))
plt.scatter(monthly_aggregated_data['month'], monthly_aggregated_data['Rainfall'], s=10, alpha=0.7, c='blue')
plt.xlabel('Date')
plt.ylabel('Rainfall (mm)') # Corrected y-axis label
plt.title('Scatter Plot of Rainfall vs. Temperature')
st.pyplot(fig_scatter)

# Interactive Plots with Plotly
st.subheader("Interactive Temperature Trends Across Regions (Plotly)")
fig_plotly_temp = px.line(weather_data, x='date', y='Temperature', color='Region', title='Temperature Trends Across Regions')
st.plotly_chart(fig_plotly_temp)  # Use st.plotly_chart for Plotly plots


# --- Extreme Events Analysis ---
st.subheader("Extreme Weather Events Analysis")

heatwave_threshold = st.number_input("Heatwave Temperature Threshold (°C)", value=20.0)
heavy_rainfall_threshold = st.number_input("Heavy Rainfall Threshold (mm)", value=12.0)

weather_data['heatwave'] = weather_data['Temperature'] > heatwave_threshold
weather_data['heavy_rainfall'] = weather_data['Rainfall'] > heavy_rainfall_threshold

weather_data['heatwave_streak'] = weather_data['heatwave'].astype(int).groupby(weather_data['Region']).cumsum()
heatwave_events = weather_data[weather_data['heatwave_streak'] >= 3]

event_counts = weather_data.groupby('Region')[['heatwave', 'heavy_rainfall']].sum()
average_intensity = weather_data.groupby('Region')[['Temperature', 'Rainfall']].mean()

st.write("Heatwave Events (at least 3 consecutive days):")
st.write(heatwave_events)
st.write("Extreme Event Counts by Region:")
st.write(event_counts)
st.write("Average Intensity by Region:")
st.write(average_intensity)

st.subheader("Heatwaves Highlighted on Temperature Trends")
fig_heatwave_highlight = plt.figure(figsize=(12, 6))
for region in weather_data['Region'].unique():
    region_data = weather_data[weather_data['Region'] == region]
    plt.plot(region_data['date'], region_data['Temperature'], label=f'{region} Temperature')
    heatwave_days = region_data[region_data['heatwave']]
    plt.scatter(heatwave_days['date'], heatwave_days['Temperature'], color='red', label=f'{region} Heatwave')

plt.xlabel('Date')
plt.ylabel('Temperature')
plt.title('Heatwaves Highlighted on Temperature Trends')
plt.legend()
st.pyplot(fig_heatwave_highlight)

st.subheader("Timeline of Heatwave and Heavy Rainfall Events")
fig_timeline = plt.figure(figsize=(14, 7))

plt.plot(weather_data['date'], weather_data['Temperature'], label='Temperature', color='tab:red', alpha=0.7)
plt.plot(weather_data['date'], weather_data['Rainfall'], label='Rainfall', color='tab:blue', alpha=0.7)

heatwave_dates = weather_data[weather_data['heatwave']]['date']
heatwave_values = weather_data[weather_data['heatwave']]['Temperature']
plt.scatter(heatwave_dates, heatwave_values, color='red', label='Heatwave', zorder=5) #Changed color to red for heatwave

rainfall_dates = weather_data[weather_data['heavy_rainfall']]['date']
rainfall_values = weather_data[weather_data['heavy_rainfall']]['Rainfall']
plt.scatter(rainfall_dates, rainfall_values, color='blue', label='Heavy Rainfall', zorder=5)

plt.title('Timeline of Heatwave and Heavy Rainfall Events')
plt.xlabel('Date')
plt.ylabel('Values (°C for Temperature, mm for Rainfall)')
plt.legend()
plt.grid(alpha=0.5)
plt.tight_layout()
st.pyplot(fig_timeline)
