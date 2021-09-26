import streamlit as st
import pandas as pd
from util import get_data
pd.set_option('display.max_columns', None)

#put n line spaces in the sidebar
def sidebar_spaces(n):
    for i in range(n):
        st.sidebar.write('\n')

@st.cache(ttl=60*240)
def get_case_data():
    df = get_data('data.cdc.gov', '9mfq-cb36')
    df['submission_date'] = pd.to_datetime(df['submission_date'])
    return df

@st.cache(ttl=60*240)
def get_vaccination_data():
    df = get_data('data.cdc.gov', 'unsk-b7fc')
    df['date'] = pd.to_datetime(df['date'])
    df['mmwr_week'] = df['mmwr_week'].astype('int64')
    df.loc[:, 'distributed':] = df.loc[:, 'distributed':].astype('float64')
    df = df.iloc[::-1]
    df = df.set_index('date')
    return df


st.title('Covid-19: The US Numbers *')
st.sidebar.header('Display Options')

col1, col2 = st.columns([2,2])
col1.header('Cases')
col2.header('Deaths')

#get covid case data and sort by state
df = get_case_data()

#pick State in sidebar
pickState = df['state'].drop_duplicates().sort_values()
pickState = pickState.tolist()
pickState.insert(0, 'US')
default = pickState.index('US')
sidebar_spaces(3)
picked_state = st.sidebar.selectbox('Choose a state, or "US" for all states :', pickState, default)

#pick charts to show
st.sidebar.markdown("***")
pick = ['All Cases','Cases Last 60 Days','All Deaths','Deaths Last 60 Days']
opt = st.sidebar.selectbox('Choose Data for Upper Graph: ', pick, 0)

#choose state or US
if picked_state != 'US':
    #show charts forindividual state
    #pivot data making state columns
    dfState = df.pivot(index='submission_date', columns='state',values='new_case')
    dfState_dead = df.pivot(index='submission_date', columns='state',values='new_death')
    
    #create column with 7 day moving average
    dfState['7 Day Avg'] = dfState[picked_state].rolling(7).mean().round(1)
    dfState_dead['7 Day Avg'] = dfState_dead[picked_state].rolling(7).mean().round(1)
    
    #use data from last 60 days
    dfState60 = dfState.tail(60)
    dfState_dead60 = dfState_dead.tail(60)

    #change date format so time is not shown
    dfState2 = dfState.reset_index()
    dfState2['sDate'] = dfState2['submission_date'].astype('str')
    dfState3 = dfState2.set_index('sDate').drop('submission_date', axis=1)
    dfState360 = dfState3.tail(60)
    dfState2_dead = dfState_dead.reset_index()
    dfState2_dead['sDate'] = dfState2_dead['submission_date'].astype('str')
    dfState3_dead = dfState2_dead.set_index('sDate').drop('submission_date', axis=1)
    dfState3_dead60 = dfState3_dead.tail(60)

    #show state case data in dataframe
    #col1.dataframe(dfState3[[picked_state,'7 Day Avg']],700,200)
    #col2.dataframe(dfState3_dead[[picked_state,'7 Day Avg']],700,200)

    #show state case data in line chart
    #st.line_chart(dfState['7 Day Avg'])
    
    #show chart based on choice
    if opt == 'All Cases':
        st.line_chart(dfState['7 Day Avg'])
        col1.dataframe(dfState3[[picked_state,'7 Day Avg']],700,200)
        col2.dataframe(dfState3_dead[[picked_state,'7 Day Avg']],700,200)

    elif opt == 'Cases Last 60 Days':   
        st.line_chart(dfState60['7 Day Avg'])
        col1.dataframe(dfState360[[picked_state,'7 Day Avg']],700,200)
        col2.dataframe(dfState3_dead60[[picked_state,'7 Day Avg']],700,200)

        
    elif opt == 'All Deaths':
        st.line_chart(dfState_dead['7 Day Avg'])
        col1.dataframe(dfState3[[picked_state,'7 Day Avg']],700,200)
        col2.dataframe(dfState3_dead[[picked_state,'7 Day Avg']],700,200)
        
    elif opt == 'Deaths Last 60 Days':
        st.line_chart(dfState_dead60['7 Day Avg'])
        col1.dataframe(dfState360[[picked_state,'7 Day Avg']],700,200)
        col2.dataframe(dfState3_dead60[[picked_state,'7 Day Avg']],700,200)
    

else:
    #show charts for US
    #get new cases
    df_us = df.fillna(0)
    df_us = df_us.astype({'new_case': 'float64'})
    df_us = df_us.astype({'new_case': 'int64'})
    df_us = df_us.groupby('submission_date').agg(Cases=('new_case','sum'))
    df_us['Cases'] = df_us['Cases'].astype('int64')
    df_us['7 Day Avg'] = df_us.rolling(7).mean().round(1)
    df_us60 = df_us.tail(60)

    df_us2 = df_us.reset_index()
    df_us2['sDate'] = df_us2['submission_date'].astype('str')
    df_us3 = df_us2.set_index('sDate').drop('submission_date', axis=1)
    df_us360 = df_us3.tail(60)
    
    #get new deaths
    df_us_dead = df.fillna(0)
    df_us_dead = df_us_dead.astype({'new_death': 'float64'})
    df_us_dead = df_us_dead.astype({'new_death': 'int64'})
    df_us_dead = df_us_dead.groupby('submission_date').agg(Deaths=('new_death','sum'))
    df_us_dead['Deaths'] = df_us_dead['Deaths'].astype('int64')
    df_us_dead['7 Day Avg'] = df_us_dead.rolling(7).mean().round(1)
    df_us_dead60 = df_us_dead.tail(60)

    df_us_dead2 = df_us_dead.reset_index()
    df_us_dead2['sDate'] = df_us_dead2['submission_date'].astype('str')
    df_us_dead3 = df_us_dead2.set_index('sDate').drop('submission_date', axis=1)
    df_us_dead360 = df_us_dead3.tail(60)
    
    #show chart based on choice
    if opt == 'All Cases':
        st.line_chart(df_us)
        col1.dataframe(df_us3,700,200)
        col2.dataframe(df_us_dead3,700,200)
        
    elif opt == 'Cases Last 60 Days':   
        st.line_chart(df_us60)
        col1.dataframe(df_us360,700,200)
        col2.dataframe(df_us_dead360,700,200)

    elif opt == 'All Deaths':
        st.line_chart(df_us_dead)
        col1.dataframe(df_us3,700,200)
        col2.dataframe(df_us_dead3,700,200)
        
    elif opt == 'Deaths Last 60 Days':
        st.line_chart(df_us_dead60)
        col1.dataframe(df_us360,700,200)
        col2.dataframe(df_us_dead360,700,200)
        
col1.subheader(opt + ' for ' + picked_state) 

st.header('Immunizations')

dfv = get_vaccination_data()
dfv.rename(columns = {'location':'State','administered':'All','administered_janssen':'J&J','administered_moderna':'Moderna','administered_pfizer':'Pfizer','administered_unk_manuf':'Unknown','administered_dose1_pop_pct':'First Dose','series_complete_pop_pct':'Series Complete'}, inplace = True)

#get manufacturer for graph
pickMan = ['All','J&J','Moderna','Pfizer','Unknown']

#make dataframe with only administered data
dfAdmin = dfv[['State','All','J&J','Moderna','Pfizer','Unknown']]
dfAdmin[pickMan] = dfAdmin[pickMan].astype('int64')
filt2 = dfAdmin['State'] == picked_state
dfAState = dfAdmin[filt2]

dfAState2 = dfAState.reset_index()
dfAState2['sDate'] = dfAState2['date'].astype('str')
dfAState3 = dfAState2.set_index('sDate').drop('date', axis=1)

st.dataframe(dfAState3,700,200)
st.subheader('Total Immunizations for ' + picked_state)
st.line_chart(dfAState[pickMan])

#make dataframe with percent data
dfpct = dfv[['State','First Dose','Series Complete']]
filt3 = dfpct['State'] == picked_state
dfpctState = dfpct[filt3]

#st.dataframe(dfpctState,700,200)
st.subheader('Percent of Population Immunized for ' + picked_state)
st.line_chart(dfpctState[['First Dose','Series Complete']])

      
'* from data.cdc.gov'