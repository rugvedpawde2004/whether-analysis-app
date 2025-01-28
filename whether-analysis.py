import streamlit as st
import pandas as pd

rain = pd.read_csv('pune_weather_with_regions.csv')
rain
import pandas as pd

# Load the uploaded dataset to check its structure and understand the columns for processing
import pandas as pd

# Define the file path
file_path = 'pune_weather_with_regions.csv'

# Load the dataset
weather_data = pd.read_csv(file_path)

# Display the first few rows of the dataset
weather_data.head(), weather_data.info()


# Convert 'date' column to datetime format
weather_data['date'] = pd.to_datetime(weather_data['date'], format='%d-%m-%Y')

# Add a 'month' column for grouping
weather_data['month'] = weather_data['date'].dt.to_period('M')

# Group by 'month' and aggregate numerical values (average for temperature, humidity, and rainfall)
monthly_aggregated_data = weather_data.groupby('month').agg({
    'Temperature': 'mean',
    'Humidity': 'mean',
    'Rainfall': 'mean'
}).reset_index()

# Convert 'month' back to a standard datetime format for clarity
monthly_aggregated_data['month'] = monthly_aggregated_data['month'].dt.to_timestamp()

# Display the aggregated data
monthly_aggregated_data

import matplotlib.pyplot as plt
plt.figure(figsize=(20,12))
plt.plot(monthly_aggregated_data['month'], monthly_aggregated_data['Temperature'], marker='*', color='blue', label='Temperature (°C)')
plt.title('Temperature Trends Over Time', fontsize=16)
plt.xlabel('date', fontsize=12)
plt.ylabel('Values', fontsize=12)
plt.grid(alpha=0.5)
plt.legend(fontsize=11)
plt.tight_layout()
plt.show()


plt.figure(figsize=(20,12))
plt.plot(monthly_aggregated_data['month'], monthly_aggregated_data['Rainfall'], marker='>', color='red', label='Rainfall (mm)')
plt.title('Rainfall Trends Over Time', fontsize=16)
plt.xlabel('date', fontsize=12)
plt.ylabel('Values', fontsize=12)
plt.grid(alpha=0.5)
plt.legend(fontsize=11)
plt.tight_layout()
plt.show()


# Bar graph for Rainfall Over Time
plt.figure(figsize=(10, 6))
sns.barplot(x=monthly_aggregated_data['month'].dt.month, y=monthly_aggregated_data['Rainfall'], palette="Blues_d")
plt.title('Average Monthly Rainfall', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Rainfall (mm)', fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.show()


g = sns.FacetGrid(weather_data, col='Region', col_wrap=3, height=4, sharey=True)
g.map(sns.lineplot, 'date', 'Temperature')
g.set_titles('{col_name}')
g.set_axis_labels('Date', 'Temperature')
plt.show()


plt.figure(figsize=(10, 6))
plt.scatter(monthly_aggregated_data['month'], monthly_aggregated_data['Rainfall'],  s=10 ,alpha=0.7, c='blue')  # Replace 'x_column' and 'y_column'
plt.xlabel('Date')  # Replace with your column name or label
plt.ylabel('Temp')  # Replace with your column name or label
plt.title('Scatter Plot')
plt.show()


#grouped_data = cleaned_data.groupby(['Region', 'date'])['Temperature'].mean().reset_index()

#print(cleaned_data)
import plotly.express as px

# Interactive line plot
fig = px.line(weather_data, x='date', y='Temperature', color='Region', title='Temperature Trends Across Regions')
fig.show()

# Interactive grouped bar chart
fig = px.bar(grouped_data, x='date', y='Temperature', color='Region', barmode='group', title='Average Temperature by Year')
fig.show()


# Define thresholds
heatwave_threshold = 20  # Example: Temperature > 40°C
heavy_rainfall_threshold = 12  # Example: Rainfall > 50 mm/day
weather_data = pd.read_csv('C:/Users/admin/neuai/Project_01/pune_weather_with_regions.csv')
# Convert 'date' column to datetime format
weather_data['date'] = pd.to_datetime(weather_data['date'], format='%d-%m-%Y')

# Add a 'month' column for grouping
weather_data['month'] = weather_data['date'].dt.to_period('M')

# Add extreme event columns
weather_data['heatwave'] = weather_data['Temperature'] > heatwave_threshold
weather_data['heavy_rainfall'] = weather_data['Rainfall'] > heavy_rainfall_threshold


# Identify consecutive heatwave days
weather_data['heatwave_streak'] = weather_data['heatwave'].astype(int).groupby(weather_data['Region']).cumsum()

# Filter for events lasting more than 3 days
heatwave_events = weather_data[weather_data['heatwave_streak'] >= 3]
print(heatwave_events)


# Count events by region
event_counts = weather_data.groupby('Region')[['heatwave', 'heavy_rainfall']].sum()
print(event_counts)

# Average intensity
average_intensity = weather_data.groupby('Region')[['Temperature', 'Rainfall']].mean()
print(average_intensity)


plt.figure(figsize=(12, 6))
for region in weather_data['Region'].unique():
    region_data = weather_data[weather_data['Region'] == region]
    plt.plot(region_data['date'], region_data['Temperature'], label=f'{region} Temperature')
    heatwave_days = region_data[region_data['heatwave']]
    plt.scatter(heatwave_days['date'], heatwave_days['Temperature'], color='red', label=f'{region} Heatwave')

plt.xlabel('Date')
plt.ylabel('Temperature')
plt.title('Heatwaves Highlighted on Temperature Trends')
plt.legend()
plt.show()


import matplotlib.pyplot as plt

# Convert the 'date' column to datetime format (if not already done)
weather_data['date'] = pd.to_datetime(weather_data['date'])

# Plot the temperature and rainfall over time
plt.figure(figsize=(14, 7))

# Temperature line plot
plt.plot(weather_data['date'], weather_data['Temperature'], label='Temperature', color='tab:red', alpha=0.7)

# Rainfall line plot
plt.plot(weather_data['date'], weather_data['Rainfall'], label='Rainfall', color='tab:blue', alpha=0.7)

# Highlight heatwave events
heatwave_dates = weather_data[weather_data['heatwave']]['date']
heatwave_values = weather_data[weather_data['heatwave']]['Temperature']
plt.scatter(heatwave_dates, heatwave_values, color='blue', label='Heatwave', zorder=5)

# Highlight heavy rainfall events
rainfall_dates = weather_data[weather_data['heavy_rainfall']]['date']
rainfall_values = weather_data[weather_data['heavy_rainfall']]['Rainfall']
plt.scatter(rainfall_dates, rainfall_values, color='blue', label='Heavy Rainfall', zorder=5)

# Add labels, title, and legend
plt.title('Timeline of Heatwave and Heavy Rainfall Events')
plt.xlabel('Date')
plt.ylabel('Values (°C for Temperature, mm for Rainfall)')
plt.legend()
plt.grid(alpha=0.5)
plt.tight_layout()

# Show the plot
plt.show()


