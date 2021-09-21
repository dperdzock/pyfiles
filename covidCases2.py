import streamlit as st
import pandas as pd
from util import get_data

st.set_page_config(layout = 'wide')

st.title('Covid-19 Cases / Deaths in USA *')
col1, col2 = st.columns([2,2])

@st.cache
def get_vaccination_data():
    df = get_data('data.cdc.gov', '9mfq-cb36')
    df['submission_date'] = pd.to_datetime(df['submission_date'])
    return df

pickMan = ['All Cases','Cases Last 60 Days','All Deaths','Deaths Last 60 Days']
optMan = st.sidebar.selectbox('Graph to Display: ', pickMan, 0)

df = get_vaccination_data()

#get new cases
df = df.fillna(0)
dff = df.astype({'new_case': 'float64'})
dfi = dff.astype({'new_case': 'int64'})
dfit = dfi.groupby('submission_date').agg(Cases=('new_case','sum'))
dfit['Cases'] = dfit['Cases'].astype('int64')
dfit['7 Day Avg'] = dfit.rolling(7).mean().round(1)
dfit60 = dfit.tail(60)

dfit2 = dfit.reset_index()
dfit2['sDate'] = dfit2['submission_date'].astype('str')
dfit3 = dfit2.set_index('sDate').drop('submission_date', axis=1)
dfit360 = dfit3.tail(60)

#get new deaths
dfd = df.astype({'new_death': 'float64'})
dfdi = dfd.astype({'new_death': 'int64'})
dfdt = dfdi.groupby('submission_date').agg(Deaths=('new_death','sum'))
dfdt['Deaths'] = dfdt['Deaths'].astype('int64')
dfdt['7 Day Avg'] = dfdt.rolling(7).mean().round(1)
dfdt60 = dfdt.tail(60)

dfdt2 = dfdt.reset_index()
dfdt2['sDate'] = dfdt2['submission_date'].astype('str')
dfdt3 = dfdt2.set_index('sDate').drop('submission_date', axis=1)
dfdt360 = dfdt3.tail(60)

#show chart based on choice
if optMan == 'All Cases':
    st.line_chart(dfit)
    col1.dataframe(dfit3,700,200)
    col2.dataframe(dfdt3,700,200)
elif optMan == 'Cases Last 60 Days':   
    st.line_chart(dfit60)
    col1.dataframe(dfit360,700,200)
    col2.dataframe(dfdt360,700,200)
elif optMan == 'All Deaths':
    st.line_chart(dfdt)
    col1.dataframe(dfit3,700,200)
    col2.dataframe(dfdt3,700,200)
elif optMan == 'Deaths Last 60 Days':
    st.line_chart(dfdt60)
    col1.dataframe(dfit360,700,200)
    col2.dataframe(dfdt360,700,200)
    
'* from data.cdc.gov'    
    