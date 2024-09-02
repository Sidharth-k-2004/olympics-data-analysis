import pandas as pd
import numpy as np


def fetch_medal_tally(df,year,country):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag=0
    if year=="Overall" and country =="Overall":
        temp_df=medal_df
    if year=="Overall" and country !="Overall":
        flag=1
        temp_df=medal_df[medal_df['region']==country]
    if year!="Overall" and country =="Overall":
        temp_df=medal_df[medal_df['Year']==int(year)]
    if year!="Overall" and country !="Overall":
        temp_df=medal_df[(medal_df['region']==country) & (medal_df['Year']==int(year))]

    if flag==1:
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['Total']=x['Gold']+x['Silver']+x['Bronze']

    return x

def medalTally(df):
    country_wise_medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    country_wise_medal_tally=country_wise_medal_tally.groupby('NOC').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    country_wise_medal_tally['Total']=country_wise_medal_tally['Gold']+country_wise_medal_tally['Silver']+country_wise_medal_tally['Bronze']
    return country_wise_medal_tally

def countryYearList(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    country=np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')
    return years,country

def overtime(df,col):
    participated_nations_over_time = df.drop_duplicates(['Year', col])

    participated_nations_over_time = participated_nations_over_time['Year'].value_counts().reset_index()

    participated_nations_over_time.columns = ['Year', col]

    participated_nations_over_time = participated_nations_over_time.sort_values('Year')

    return participated_nations_over_time





def heat_map_sport_overtime(df):
    pivot_table = df.drop_duplicates(['Year', 'Event', 'Sport']).pivot_table(
    index='Sport', columns='Year', values='Event', aggfunc='count'
).fillna(0)
    return pivot_table

def most_successful(df, sport='Overall'):
    # Filter out rows where 'Medal' is NaN
    temp_df = df.dropna(subset=['Medal'])
    
    # If a specific sport is selected, filter by that sport
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    
    # Count the number of medals won by each athlete
    medal_counts = temp_df['Name'].value_counts().reset_index().head(15)
    
    # Rename the columns for clarity
    medal_counts.columns = ['Athlete', 'Medal Count']
    
    # Merge with original dataframe to get additional details
    x = medal_counts.merge(df, left_on='Athlete', right_on='Name', how='left')[
        ['Athlete', 'Medal Count', 'Sport', 'region']
    ].drop_duplicates('Athlete')
    
    # Rename the 'region' column to 'Country' for clarity
    x = x.rename(columns={'region': 'Country'})
    
    return x

def yearwise_medal_tally(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['region']==country]
    final_df=new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def countrywise_medal_tally_heatmap(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['region']==country]
    pt=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt

def most_successful_country_wise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    
    temp_df = temp_df[temp_df['region'] == country]
    
    medal_counts = temp_df['Name'].value_counts().reset_index().head(10)
    
    medal_counts.columns = ['Athlete', 'Medal Count']
    
    # Merge with original dataframe to get additional details
    x = medal_counts.merge(df, left_on='Athlete', right_on='Name', how='left')[
        ['Athlete', 'Medal Count', 'Sport']
    ].drop_duplicates('Athlete')
    
    x = x.rename(columns={'region': 'Country'})
    
    return x

def weight_height_sport(df,sport):
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna('No medal',inplace=True)
    if sport!='Overall':
        temp_df=athlete_df[athlete_df['Sport']==sport]
        return temp_df
    else:
        return athlete_df

def men_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    
    # Count the number of male athletes per year
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    
    # Count the number of female athletes per year
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    
    # Merge the two DataFrames on 'Year'
    final = men.merge(women, on='Year', how='left')
    
    # Rename columns for clarity
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    
    # Replace NaN values with 0
    final.fillna(0, inplace=True)
    
    return final
