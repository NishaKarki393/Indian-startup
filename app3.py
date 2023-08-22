import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import streamlit as st
import plotly.graph_objects as go

df=pd.read_csv('cleanedStartupFile.csv')
df['date']=pd.to_datetime(df['date'],format='%d-%m-%Y')
df.set_index('date',inplace=True)

# --> cleaning remaining data
df = df.replace(['Accel Partners India', 'Accel Partner', 'Accel Partners'], 'Accel Partners', regex=True)
df = df.replace(['Accel Partnerss'], 'Accel Partners', regex=True)
df = df.replace(['Accel Partners,'], 'Accel Partners', regex=True)


st.sidebar.header('Over Analysis')
option=st.sidebar.selectbox('Choose One',['Project Details','Overall Analysis','Startups','Investors'])



st.header('Indian Startup Funding Analysis (2015-2020)')

if option=='Overall Analysis':
    st.header('Overall Analysis')

    price=df['amount'].sum()
    maximum=df['amount'].max()
    average=round(df['amount'].mean(),2)
    total_funded=df['amount'].count()

    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric('Total',f"{price} cr")

    with col2:
        st.metric('Max',f"{maximum} cr")

    with col3:
        st.metric('Avg',f"{average} cr")

    with col4:
        st.metric('Startup Funded',f"{total_funded}")

    st.write(""" """)
    st.write(""" """)
    st.write(""" """)
    st.write(""" """)

    st.header("MOM Line plot for each company 2015-2020")

    option2 = st.selectbox('Options',['Total Funding','Counts'])

    if option2=='Total Funding':
        temp_df = df.resample('M')['amount'].sum().to_frame().reset_index()
        temp_df['date'] = temp_df['date'].astype('str')
        temp_df['date'] = temp_df['date'].str[0:7]
        temp_df.set_index('date', inplace=True)

        # st.markdown('## MOM total funding 2015-2020')   
        fig,ax = plt.subplots(figsize=(15,8))
        ax.plot(temp_df.index, temp_df.values)
        plt.xticks(rotation=90)
        plt.title('MOM total funding  2015-2020')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        st.pyplot(fig) 


    if option2 == 'Counts':
        temp_df2 = df.resample('M')['startup'].count().to_frame().reset_index()
        temp_df2['date'] = temp_df2['date'].astype('str')
        temp_df2['date'] = temp_df2['date'].str[0:7]
        temp_df2.set_index('date', inplace=True)

        fig,ax = plt.subplots(figsize=(15,8))
        ax.plot(temp_df2.index, temp_df2.values)
        plt.xticks(rotation=90)
        plt.title('MOM total  counts of startups 2015-2020')
        plt.xlabel('Date')
        plt.ylabel('Count')

        st.pyplot(fig) 


    st.write(""" """)
    st.write(""" """)
    st.write(""" """)
    st.write(""" """)

    st.subheader('Sectorwise analysis pie diagram 2015-2020')
    option3 = st.selectbox('Options',['Total Sector Funding', 'Sector Counts'])

    if option3 ==  'Total Sector Funding':
        temp_df4 = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(7)
        fig,ax = plt.subplots(figsize=(5,4))
        ax.pie(temp_df4.values,labels = temp_df4.index, autopct = '%0.1f%%',textprops={'fontsize': 5})
        plt.title('Top 7 sectors which got maximum funding',  fontsize=5)

        st.pyplot(fig) 

    
    if option3 == 'Sector Counts':
        temp_df3 = df['vertical'].value_counts().head(7)
        fig,ax = plt.subplots(figsize=(5,4))
        ax.pie(temp_df3.values,labels = temp_df3.index, autopct = '%0.1f%%',textprops={'fontsize': 5})
        plt.title('Top 7 sectors by count', fontsize=5)
        st.pyplot(fig) 


    col1,col2 = st.columns(2)

    with col1:
            # displaying top investor
        st.header("Types of funding")
        funding_types = sorted(df['round'].unique())
        funding_types_ser = pd.Series(funding_types, name='Types of Funding')
        st.dataframe(funding_types_ser,use_container_width=False, width=400)




    with col2:
    #bar plot
        st.header('Top 10 City wise funding')

        temp_df5 = df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10)
        fig,ax = plt.subplots(figsize=(10,10))
        ax.bar(temp_df5.index, temp_df5.values )
        plt.title('top 10 cities funded')
        plt.xlabel('City')
        plt.ylabel('fund')
        plt.xticks(rotation=90)
        st.pyplot(fig) 



    st.header('Top Investor')
    max_amount = df['amount'].max()
    top_investor = (df[df['amount'] == max_amount][['investors','amount']]).set_index('investors')
    st.dataframe(top_investor, use_container_width=False, width=250)


elif option=='Startups':
    startup_list = sorted(df['startup'].unique())  #cal
    selected_startup=st.sidebar.selectbox('option',startup_list)
    btn=st.sidebar.button("Find the startup")
