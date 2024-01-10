

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

# Read data from a CSV file
#file_path =('owid-covid-data.csv')
df = pd.read_csv("owid-covid-data.csv")
# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])
# Remove rows where continent information is missing
df = df.dropna(subset=['continent'])
# Load the world map data using geopandas
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Create subplots
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 11))

# Set the title for the entire figure
fig.suptitle('COVID-19 Analysis\n',fontweight='bold', fontsize = 24, y = 0.95)

fig.text(0.9,0.95,"Studentname: Kamali Bakthavatchalam\n StudentId: 22081557\n\n",ha='right',va='top')
# Plot total COVID-19 cases over time
total_cases_over_time = df.groupby('date')['total_cases'].sum().reset_index()
axes[0, 0].plot(total_cases_over_time['date'], total_cases_over_time['total_cases'], color='blue')
axes[0, 0].set_xlabel('Date')
axes[0, 0].set_ylabel('Total COVID-19 Cases')
axes[0, 0].set_title('Fig (a). Total COVID-19 Cases Over Time')
axes[0, 0].grid(axis='y')


# Plot Total Covid-19 Cases (%) by Continent

continent_summary = df.groupby('continent')['total_cases'].sum().reset_index()
world = world.merge(continent_summary, how='left', left_on='continent', right_on='continent')
world = world.dissolve(by='continent', aggfunc='sum')
world['total_cases_percentage'] = (world['total_cases'] / world['total_cases'].sum()) * 100

# Plotting the choropleth map with continent names and percentages on axes[0, 1]
world.boundary.plot(ax=axes[0, 1])  # Plot country boundaries
world.plot(column='total_cases_percentage', cmap='YlOrRd', ax=axes[0, 1], legend=True,
           legend_kwds={'label': "Total Cases (%) by Continent", 'orientation': "horizontal"})

# Adding text labels for continent names and percentages
for idx, row in world.iterrows():
    axes[0, 1].text(row.geometry.centroid.x, row.geometry.centroid.y,
                    f"{idx} ({row['total_cases_percentage']:.2f}%)",
                    fontsize=8, ha='center', va='center', color='black',fontweight='bold')

axes[0, 1].set_title("Fig (b).Total Cases Percentage by Continent")
axes[0, 1].axis('off') 
 # Turn off axis

# Plot Top 10 countries with most death rate
# This section assumes the dataframe 'df' is already filtered and contains the required data
names_to_exclude = ['World', 'Asia', 'High income', 'Europe', 'European Union',
                    'Upper middle income', 'North America', 'Africa', 'South America',
                    'Lower middle income']
df = df[~df['location'].isin(names_to_exclude)]
total_deaths_by_country = df.groupby('location')['total_deaths'].max()
top_10_deaths = total_deaths_by_country.nlargest(10)
bars = axes[1, 0].bar(top_10_deaths.index, top_10_deaths.values, color='skyblue')
for bar in bars:
    yval = bar.get_height() / 1000  # Convert values to 'k'
    axes[1, 0].text(bar.get_x() + bar.get_width()/2, yval, f"{yval:.1f}k", ha='center', va='bottom', color='maroon')
axes[1, 0].set_xlabel('Countries')
axes[1, 0].set_ylabel('Number of Deaths')
axes[1, 0].set_title('Fig (c). Top Countries with the Highest Covid-19 Fatality')
axes[1, 0].set_xticklabels(top_10_deaths.index, rotation=45)
axes[1, 0].grid(axis='y')


# Plotting the trend of people vaccinated and total deaths for the United States on axes[1, 1]
data_us = df[df['location'] == 'United States']
grouped_data = data_us.groupby('date').agg({
    'total_cases': 'max',
    'people_vaccinated': 'max'
}).reset_index()

axes[1, 1].plot(grouped_data['date'], grouped_data['people_vaccinated'], label='People Vaccinated', color='blue')
axes[1, 1].plot(grouped_data['date'], grouped_data['total_cases'], label='Total Cases', color='red')

axes[1, 1].set_xlabel('Date')
axes[1, 1].set_ylabel('Count')
axes[1, 1].set_title('Fig (d).Trend of People Vaccinated and Total Cases in the United States')
axes[1, 1].legend()
axes[1, 1].grid()




# Adding text at the end of the figure
fig.text(0.01, 0.01, 'The trend of COVID-19 cases shows a rise until July 2023 (Fig a). In Fig (b), Asia and Europe account for over 45% and 37% of global COVID-19 cases, respectively. \nAmong countries, the United States has the highest death rate at 1136k, followed by Brazil and India (Fig c). In the United States, the reduction in cases corresponds to increased vaccination (Fig d). \nThe emergence of the Omicron variant caused a surge in cases, affecting mainly non-vaccinated individual'
, ha='left',va='bottom', fontsize=9, color='grey')

# Adjust the spacing between subplots and footer text
plt.subplots_adjust(bottom=0.2)
# Adjust layout
plt.tight_layout(pad=4.2)
plt.savefig("22081557.png", dpi=300)