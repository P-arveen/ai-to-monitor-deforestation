import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os







def data_file():

    base_dir = r'D:\def1\data'
    file_name = 'goal15.forest_shares.csv'
    file_path = os.path.join(base_dir, file_name)
    #Load the dataset and remove missing data
    def_df = pd.read_csv(file_path)
    def_df = def_df.dropna()
    def_df

    print(def_df.head())
    print(def_df.shape)



    #Create a dictionary with GDP data
    gdp_data = {
        'Continent': ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America', 'World'],
        'GDP (2020)': [5.079, 13.725, 38.856, 45.284, 37.947, 14.679, 17.253],
    }
    #Create a DataFrame set 'Continent' column as the index
    gdp_df = pd.DataFrame(gdp_data)
    gdp_df.set_index('Continent', inplace=True)
    gdp_df



    #Plot a pie chart
    gdp_df_for_chart = gdp_df.drop('World')
    custom_colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6']

    plt.figure(figsize=(8, 8))
    plt.pie(gdp_df_for_chart['GDP (2020)'], labels=gdp_df_for_chart.index, autopct='%.1f%%', startangle=140, colors=custom_colors)
    plt.title('GDP per capita by Continent for the Year 2020')
    plt.axis('equal')
    plt.savefig("gdp_pie_chart.png", dpi=300)  # Save as PNG
    plt.show()


    country_to_continent = {
        'BRA': 'South America',
        'CAN': 'North America',
        'IND': 'Asia',
        'CHN': 'Asia',
        'DEU': 'Europe',
        'USA': 'North America',
        'AUS': 'Oceania',
        'ZAF': 'Africa',
        # Add more countries as needed
    }

    #Add a new column 'continent'
    def_df = def_df.copy()
    def_df['continent'] = def_df['iso3c'].map(country_to_continent)

    #Group data by continent, calculate summary statistics for 'trend', display grouped data
    grouped_def = def_df.groupby('continent')['trend'].describe()

    #Create a boxplot
    transposed_def = grouped_def.transpose()

    custom_colors = ['#8c510a','#d8b365','#f6e8c3','#f5f5f5','#c7eae5','#5ab4ac','#01665e'] 
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=transposed_def.iloc[1:], palette=custom_colors)
    plt.title('Summary Statistics of Change in Forest Area by Continent (2020)')
    plt.xlabel('Statistical Measure')
    plt.ylabel('Change in Forest Area')
    plt.xticks(rotation=45)
    plt.savefig("forest_area_barplot.png", dpi=300)  # Save as PNG
    plt.show()

    #Calculate mean trend for each continent
    continent_stats = def_df.groupby('continent')['trend'].mean()
    continent_stats = continent_stats.reset_index()

    #Create a bar plot for mean deforestation trends by continent
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.barplot(x='continent', y='trend', data=continent_stats, errorbar=None, palette=custom_colors)
    plt.title('Change in Forest Area by Continent')
    plt.xlabel('')
    plt.ylabel('Change in Forest Area')
    plt.xticks(rotation=45)
    plt.savefig("forest_area_barplot1.png", dpi=300)  # Save as PNG
    plt.show()
    
    
if __name__ == "__main__":
    data_file()
