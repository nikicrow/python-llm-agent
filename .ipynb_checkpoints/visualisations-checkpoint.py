import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.title('Ember data')

def create_bar_chart_with_rolling_average(x,y,
                                          x_colname,y_colname,
                                          x_title,y_title,
                                          title,period=7):
    df = pd.DataFrame(x).join(pd.DataFrame(y))
    df['rolling_average'] = y.rolling(window=period).mean()

    fig = px.bar(df, x=x_colname, y=y_colname, labels={x_colname: x_title, y_colname: y_title}, title=title)
    fig.add_scatter(x=df[x_colname], y=df['rolling_average'], mode='lines', name='Rolling Average')

    st.plotly_chart(fig)


def create_scatter_plot_with_rolling_average(x,y,
                                          x_colname,y_colname,
                                          x_title,y_title,
                                          title,period=7):
    df = pd.DataFrame(x).join(pd.DataFrame(y))
    df['rolling_average'] = y.rolling(window=period).mean()

    fig = px.scatter(df, x=x_colname, y=y_colname, labels={x_colname: x_title, y_colname: y_title}, title=title)
    fig.add_scatter(x=df[x_colname], y=df['rolling_average'], mode='lines', name='Rolling Average')

    st.plotly_chart(fig)

def create_histogram_with_colours(data,x_label,colour_label,x_title,title):
    fig = px.histogram(data, 
                       x=x_label, 
                       color=colour_label, 
                       title=title,
                       labels={x_label: x_title}, 
                       nbins=30, barmode='overlay')
    st.plotly_chart(fig)

def create_boxplot(data,x_label,y_label,x_title,y_title,title):
    # Create the boxplot chart
    fig = px.box(data, 
                 x=x_label, y=y_label, 
                 title=title,
                labels={x_label: x_title, y_label: y_title})

    # Display the chart using Streamlit
    st.plotly_chart(fig)

ember_sleep_df = pd.read_csv('data/ember_sleep_30march_updated.csv')
ember_sleep_df['sleep_date'] = pd.to_datetime(ember_sleep_df['sleep_date'])
fixed_date = pd.to_datetime('2023-08-18')
# Calculate months since birth
ember_sleep_df['months_since_birth'] = (ember_sleep_df['sleep_date'].dt.year - fixed_date.year) * 12 + (ember_sleep_df['sleep_date'].dt.month - fixed_date.month)

nap_data = ember_sleep_df[ember_sleep_df['night_sleep'] == False][['days_since_birth', 'hours_duration']].groupby('days_since_birth').mean()
nap_data = nap_data.reset_index()
create_bar_chart_with_rolling_average(nap_data['days_since_birth'], nap_data['hours_duration'],
                                      'days_since_birth','hours_duration',
                                      'Days since birth','Average nap duration (hours)',
                                      'Average nap duration vs days since birth',14)
total_sleep_data = ember_sleep_df[['days_since_birth', 'hours_duration']].groupby('days_since_birth').sum()
total_sleep_data = total_sleep_data.reset_index()
create_bar_chart_with_rolling_average(total_sleep_data['days_since_birth'],total_sleep_data['hours_duration'],
                                      'days_since_birth','hours_duration',
                                      'Days since birth','Total sleep duration (hours)',
                                      'Total sleep duration per day vs days since birth',14)
create_scatter_plot_with_rolling_average(total_sleep_data['days_since_birth'],total_sleep_data['hours_duration'],
                                      'days_since_birth','hours_duration',
                                      'Days since birth','Total sleep duration (hours)',
                                      'Total sleep duration per day vs days since birth',14)

nap_month_data = ember_sleep_df[ember_sleep_df['night_sleep'] == False][['months_since_birth', 'hours_duration']]
create_histogram_with_colours(nap_month_data,
                              'hours_duration','months_since_birth',
                              'Nap duration (hours)',
                              'Nap duration by month')


create_boxplot(nap_month_data,
               'months_since_birth','hours_duration',
               'Months since birth','Nap duration (hours)',
               'Nap duration in hours by month')

wake_month_data = ember_sleep_df[ember_sleep_df['night_sleep'] == False][['months_since_birth', 'wake_window_hours']]

create_boxplot(wake_month_data,
               'months_since_birth','wake_window_hours',
               'Months since birth','Wake window (hours)',
               'Wake window in hours by month')


import pandas as pd 
import matplotlib.pyplot as plt
# Generate some sample data
data = { 'days_since_birth': [1, 1, 1, 2, 2, 2, 3, 3, 3], 'time_24_hour': ['10:00:00', '13:00:00', '16:00:00', '09:00:00', '12:00:00', '15:00:00', '08:00:00', '11:00:00', '14:00:00'], 'duration': [40, 90, 60, 50, 120, 60, 30, 60, 90] }

df = pd.DataFrame(data)

#plot_broken_barh(df)
#def plot_broken_barh(data): 
fig, ax = plt.subplots()

for index, row in df.iterrows():
    y = pd.to_datetime(row['time_24_hour']).hour
    x = row['days_since_birth']
    duration = row['duration']

    ax.broken_barh([(x, duration)], (y, 1), facecolors='blue')

ax.set_xlabel('Days Since Birth')
ax.set_ylabel('Time of Day (24-hour format)')
ax.set_title('Activity Timeline')

plt.show()

