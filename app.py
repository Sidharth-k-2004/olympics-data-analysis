import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import preprocess_summer, preprocess_winter, medal_tally
import plotly.express as px
import plotly.figure_factory as ff
# Load data
df = pd.read_csv("athlete_events.csv")
df_region = pd.read_csv("noc_regions.csv")

# Preprocess data for Summer and Winter events
df_summer = preprocess_summer.preprocess_summer(df, df_region)
df_winter = preprocess_winter.preprocess_winter(df, df_region)

# Set page configuration
st.set_page_config(page_icon="📊", layout="wide")

# Add custom CSS to style the background and fonts
st.markdown(
    """
    <style>
    /* Background color */
    .stApp {
        background-color: #8A2BE2;
    }
    
    /* Font styling */
    .title {
        font-family: 'Arial';
        color: white;
        text-align: center;
        font-size: 3rem;
    }
    
    .st-radio {
        color: white;
        font-family: 'Verdana';
        font-size: 1.2rem;
    }
    
    /* Radio button styling */
    .stRadio > div > label {
        color: white;
    }
    
    /* Center content vertically */
    
    
    </style>
    """,
    unsafe_allow_html=True,
)
st.sidebar.title("Olymipics Analysis")
st.sidebar.image("Olympics_logo.svg.png")
# Add a sidebar with radio buttons for analysis type
options = ["Medal Tally", "Overall Analysis", "Country-wise Analysis", "Athlete-wise Analysis"]
selection = st.sidebar.radio("Select Analysis Type:", options)

# Add a section for selecting between Summer and Winter
season_options = ["Summer", "Winter"]
season_selection = st.sidebar.radio("Select Season:", season_options)


if selection == "Medal Tally":
    st.sidebar.header("Medal Tally")
    if season_selection == "Summer":
        years,country=medal_tally.countryYearList(df_summer)
        selected_year=st.sidebar.selectbox("Select Year",years)
        selected_country=st.sidebar.selectbox("Select Country",country)
        summer = medal_tally.fetch_medal_tally(df_summer,selected_year,selected_country)
        if selected_year=="Overall" and selected_country=="Overall":
            st.title("Overall Tally")
        if selected_year!="Overall" and selected_country=="Overall":
            st.title("Medal Tally in "+str(selected_year)+" Olympics")
        if selected_year=="Overall" and selected_country!="Overall":
            st.title(selected_country+" Overall Performance")
        if selected_year!="Overall" and selected_country!="Overall":
            st.title(selected_country+" performance In "+str(selected_year))
        st.table(summer)
    elif season_selection == "Winter":
        years,country=medal_tally.countryYearList(df_winter)
        selected_year=st.sidebar.selectbox("Select Year",years)
        selected_country=st.sidebar.selectbox("Select Country",country)
        winter = medal_tally.fetch_medal_tally(df_winter,selected_year,selected_country)
        if selected_year=="Overall" and selected_country=="Overall":
            st.title("Overall Tally")
        if selected_year!="Overall" and selected_country=="Overall":
            st.title("Medal Tally in "+str(selected_year)+" Olympics")
        if selected_year=="Overall" and selected_country!="Overall":
            st.title(selected_country+" Overall Performance")
        if selected_year!="Overall" and selected_country!="Overall":
            st.title(selected_country+" performance In "+str(selected_year))
        st.table(winter)

elif selection == "Overall Analysis":
    st.title("Overall Analysis")
    if season_selection == "Summer":
        editions = df_summer['Year'].unique().shape[0] - 1
        cities = df_summer['City'].unique().shape[0]
        sports = df_summer['Sport'].unique().shape[0]
        events = df_summer['Event'].unique().shape[0]
        athletes = df_summer['Name'].unique().shape[0]
        nations = df_summer['region'].unique().shape[0]

        col1, col2, col3 = st.columns(3)  # Updated to st.columns
        with col1:
            st.header("Editions")
            st.title(editions)
        with col2:
            st.header("Cities")
            st.title(cities)
        with col3:
            st.header("Sports")
            st.title(sports)

        col1, col2, col3 = st.columns(3)  # Updated to st.columns
        with col1:
            st.header("Events")
            st.title(events)
        with col2:
            st.header("Athletes")
            st.title(athletes)
        with col3:
            st.header("Nations")
            st.title(nations)
        participated_nations_over_time = medal_tally.overtime(df_winter, 'region')
        fig = px.line(participated_nations_over_time, x='Year', y='region', 
              labels={'region': 'No. of Countries'})  
        st.title("Participating Nations Over Time")
        st.plotly_chart(fig)

        events_over_time=medal_tally.overtime(df_summer,'Event')  
        fig=px.line(events_over_time,x='Year',y='Event')
        st.title("Events Over Time")
        st.plotly_chart(fig)

        athletes_over_time=medal_tally.overtime(df_summer,'Name')  
        fig=px.line(athletes_over_time,x='Year',y='Name',labels={'Name': 'Athletes'})
        st.title("Athletes Over Time")
        st.plotly_chart(fig)

        st.title("Number of Events Over Time (Every Sport)")
        pivot_table = medal_tally.heat_map_sport_overtime(df_summer)

        # Increase figure size
        plt.figure(figsize=(20, 20))
        fig, ax = plt.subplots(figsize=(16, 12))  # Adjusted size

        # Create the heatmap
        sns.heatmap(
            pivot_table, 
            annot=True, 
            fmt='g', 
            ax=ax, 
            cmap='viridis',
            cbar_kws={'shrink': 0.5},  # Shrink the color bar
            annot_kws={"size": 10}  # Decrease font size for annotations
        )

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)

        # Adjust the layout
        plt.tight_layout()

        # Display the figure in Streamlit
        st.pyplot(fig)

        st.title("Most Successful Athletes")
        sport_list=df_summer['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0,'Overall')

        selected_sport=st.selectbox('Select a Sport',sport_list)


        x=medal_tally.most_successful(df_summer,selected_sport)
        st.table(x)
        
    elif season_selection == "Winter":
        editions = df_winter['Year'].unique().shape[0] - 1
        cities = df_winter['City'].unique().shape[0]
        sports = df_winter['Sport'].unique().shape[0]
        events = df_winter['Event'].unique().shape[0]
        athletes = df_winter['Name'].unique().shape[0]
        nations = df_winter['region'].unique().shape[0]

        col1, col2, col3 = st.columns(3)  # Updated to st.columns
        with col1:
            st.header("Editions")
            st.title(editions)
        with col2:
            st.header("Cities")
            st.title(cities)
        with col3:
            st.header("Sports")
            st.title(sports)

        col1, col2, col3 = st.columns(3)  # Updated to st.columns
        with col1:
            st.header("Events")
            st.title(events)
        with col2:
            st.header("Athletes")
            st.title(athletes)
        with col3:
            st.header("Nations")
            st.title(nations)
        participated_nations_over_time = medal_tally.overtime(df_winter, 'region')
        fig = px.line(participated_nations_over_time, x='Year', y='region', 
              labels={'region': 'No. of Countries'})  
        st.title("Participating Nations Over Time")
        st.plotly_chart(fig)


        events_over_time=medal_tally.overtime(df_summer,'Event')  
        fig=px.line(events_over_time,x='Year',y='Event')
        st.title("Events Over Time")
        st.plotly_chart(fig)

        athletes_over_time=medal_tally.overtime(df_summer,'Name')  
        fig=px.line(athletes_over_time,x='Year',y='Name',labels={'Name': 'Athletes'})
        st.title("Athletes Over Time")
        st.plotly_chart(fig)

        st.title("Number of Events Over Time (Every Sport)")
        pivot_table = medal_tally.heat_map_sport_overtime(df_winter)

        # Increase figure size
        plt.figure(figsize=(20, 20))
        fig, ax = plt.subplots(figsize=(16, 12))  # Adjusted size

        # Create the heatmap
        sns.heatmap(
            pivot_table, 
            annot=True, 
            fmt='g', 
            ax=ax, 
            cmap='viridis',
            cbar_kws={'shrink': 0.5},  # Shrink the color bar
            annot_kws={"size": 10}  # Decrease font size for annotations
        )

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)

        # Adjust the layout
        plt.tight_layout()

        # Display the figure in Streamlit
        st.pyplot(fig)


        st.title("Most Successful Athletes")
        sport_list=df_winter['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0,'Overall')

        selected_sport=st.selectbox('Select a Sport',sport_list)


        x=medal_tally.most_successful(df_winter,selected_sport)
        st.table(x)


elif selection == "Country-wise Analysis":
    st.title("Country-wise Analysis")
    if season_selection == "Summer":
        country_list=df_summer['region'].dropna().unique().tolist()
        country_list.sort()
        selected_country=st.selectbox('Select a Country',country_list)

        country_df=medal_tally.yearwise_medal_tally(df_summer,selected_country)
        fig=px.line(country_df,x='Year',y='Medal')
        st.title(selected_country+" Medal Tally over years")
        st.plotly_chart(fig)

        pivot_table=medal_tally.countrywise_medal_tally_heatmap(df_summer,selected_country)
        plt.figure(figsize=(20, 20))
        fig, ax = plt.subplots(figsize=(16, 12))  # Adjusted size

        # Create the heatmap
        sns.heatmap(
            pivot_table, 
            annot=True, 
            fmt='g', 
            ax=ax, 
            cmap='viridis',
            cbar_kws={'shrink': 0.5},  # Shrink the color bar
            annot_kws={"size": 10}  # Decrease font size for annotations
        )

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)

        # Adjust the layout
        plt.tight_layout()

        # Display the figure in Streamlit
        st.title(selected_country+" excels in the following sports")
        st.pyplot(fig)

        succesful_athletes_countrywise=medal_tally.most_successful_country_wise(df_summer,selected_country)
        st.title("Most Successful Athletes for "+selected_country)
        st.table(succesful_athletes_countrywise)

    elif season_selection == "Winter":
        country_list = df_winter['region'].dropna().unique().tolist()
        country_list.sort()
        selected_country = st.selectbox('Select a Country', country_list)

        country_df = medal_tally.yearwise_medal_tally(df_winter, selected_country)
        fig = px.line(country_df, x='Year', y='Medal')
        st.title(f"{selected_country} Medal Tally over Years")
        st.plotly_chart(fig)

        pivot_table = medal_tally.countrywise_medal_tally_heatmap(df_winter, selected_country)

        if pivot_table.empty:
            st.warning(f"No medal data available for {selected_country} ")
        else:
            plt.figure(figsize=(20, 20))
            fig, ax = plt.subplots(figsize=(16, 12))  # Adjusted size

            sns.heatmap(
                pivot_table, 
                annot=True, 
                fmt='g', 
                ax=ax, 
                cmap='viridis',
                cbar_kws={'shrink': 0.5},  # Shrink the color bar
                annot_kws={"size": 10}  # Decrease font size for annotations
            )
            plt.xticks(rotation=45, ha='right', fontsize=10)
            plt.yticks(fontsize=10)
            plt.tight_layout()
            st.title(f"{selected_country} Excels in the Following Sports")
            st.pyplot(fig)

            succesful_athletes_countrywise=medal_tally.most_successful_country_wise(df_winter,selected_country)
            st.title("Most Successful Athletes for "+selected_country)
            st.table(succesful_athletes_countrywise)

elif selection == "Athlete-wise Analysis":
    if season_selection == "Summer":
        st.write(f"Displaying Athlete-wise Analysis for {season_selection} season...")
        athlete_df=df_summer.drop_duplicates(subset=['Name','region'])
        x1=athlete_df['Age'].dropna()
        x2=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
        x3=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
        x4=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
        st.title("Distribution of Age")
        fig=ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
        st.plotly_chart(fig)

        x=[]
        name=[]
        famous_sport=['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
       'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
       'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
       'Water Polo', 'Hockey', 'Rowing', 'Fencing', 
       'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
       'Tennis', 'Golf', 'Softball', 'Archery',
       'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
       'Rhythmic Gymnastics', 'Rugby Sevens', 
       'Beach Volleyball', 'Triathlon', 'Rugby',  'Polo',
        'Ice Hockey']
        for sport in famous_sport:
            temp_df=athlete_df[athlete_df['Sport']==sport]
            x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
            name.append(sport)
        fig=ff.create_distplot(x,name,show_hist=False,show_rug=False)
        st.title("Age vs Sport")
        st.plotly_chart(fig)

        sport_list=df_summer['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0,'Overall')

        selected_sport=st.selectbox('Select a Sport',sport_list)
        
        temp_df=medal_tally.weight_height_sport(athlete_df,selected_sport)
        fig, ax = plt.subplots()
        sns.scatterplot(x='Weight', y='Height', hue='Medal', style='Sex', data=temp_df, ax=ax)
        st.title("Height vs Weight")
        st.pyplot(fig)

        st.title('Men vs women')
        final=medal_tally.men_women(df_summer)
        fig=px.line(final,x='Year',y=['Male','Female'])
        st.plotly_chart(fig)


    elif season_selection == "Winter":
        st.write(f"Displaying Athlete-wise Analysis for {season_selection} season...")
        athlete_df=df_winter.drop_duplicates(subset=['Name','region'])
        x1=athlete_df['Age'].dropna()
        x2=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
        x3=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
        x4=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
        st.title("Distribution of Age")
        fig=ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
        st.plotly_chart(fig)

        x=[]
        name=[]
        famous_sport=['Speed Skating', 'Cross Country Skiing', 'Ice Hockey', 'Biathlon',
       'Alpine Skiing', 'Luge', 'Bobsleigh', 'Figure Skating',
       'Nordic Combined', 'Freestyle Skiing', 'Ski Jumping', 'Curling',
       'Snowboarding', 'Short Track Speed Skating', 'Skeleton',
       'Military Ski Patrol', 'Alpinism']
        for sport in famous_sport:
            temp_df=athlete_df[athlete_df['Sport']==sport]
            x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
            name.append(sport)
        fig=ff.create_distplot(x,name,show_hist=False,show_rug=False)
        st.title("Age vs Sport")
        st.plotly_chart(fig)

        sport_list=df_winter['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0,'Overall')

        selected_sport=st.selectbox('Select a Sport',sport_list)
        
        temp_df=medal_tally.weight_height_sport(athlete_df,selected_sport)
        fig, ax = plt.subplots()
        sns.scatterplot(x='Weight', y='Height', hue='Medal', style='Sex', data=temp_df, ax=ax)
        st.title("Height vs Weight")
        st.pyplot(fig)

        st.title('Men vs women')
        final=medal_tally.men_women(df_winter)
        fig=px.line(final,x='Year',y=['Male','Female'])
        st.plotly_chart(fig)