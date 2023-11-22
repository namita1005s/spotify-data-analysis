import streamlit as st
#run in terminal
#cd data analysis
#streamlit run dapp.py
import numpy as np
import pandas as pd
import plotly.express as px 
import seaborn as sns
st.set_page_config(layout='centered')

st.title('Data Analysis App')
def load_data():
    df = sns.load_dataset('titanic')
    return df
with st.spinner('Loading Data..'):
    df=load_data()
    st.write('🎉🎉🎉')

if st.checkbox("View All Data"):
    st.dataframe(df)

if st.checkbox('Show some statistics'):
    cat_cols=df.select_dtypes(include=np.number).columns.tolist()
    num_cols=df.select_dtypes(include=np.number).columns.tolist()
    st.text(num_cols)
    c1,c2=st.columns(2)
    c1.metric(label='Average age of passengers',
              value=df['age'].mean().astype(int))
    c2.metric(label='Average Fare',value=df['fare'].mean().astype(int),
              delta=round(df['fare'].std(),1))
    c1,c2=st.columns(2)
    c1.text('Number of Survivers')
    survivors= df['survived'].value_counts()
    c1.dataframe(survivors)
    fig=px.pie(survivors,survivors.index,survivors.values)
    c1.plotly_chart(fig,use_container_width=True)
    c2.text('Number of passengers in each class')
    classes=df['pclass'].value_counts()
    c2.dataframe(classes)
    fig=px.bar(classes,classes.index,classes.values)
    c2.plotly_chart(fig,use_container_width=True)

if st.checkbox('Visualize categorical data'):
    st.subheader('Categorical Data Visualization')
    sel_col=st.radio('Select Column', cat_cols,horizontal=True)
    sel_col_count =df[sel_col].value_counts()
    fig= px.pie(sel_col_count,sel_col_count.index,sel_col_count.values,title=f"Distribution of {sel_col}")
    st.plotly_chart(fig,use_container_width=True)

if st.checkbox('visualize numberical data'):
    graph_types=['Area','Line','Histogram','boxplot','violinplot']
    st.subheader('Numerical Data Visualization')
    sel_col=st.selectbox('Select Column',num_cols)
    graph_type=st.radio('select graph type',graph_types,horizontal=True)
    
    if graph_type==graph_types[1]:
        fig=px.line(df,y=sel_col,title=f"Line plot of {sel_col}")
        st.plotly_chart(fig,use_container_width=True)

    if graph_type==graph_types[2]:
        fig=px.histogram(df,x=sel_col,title=f"Histogram plot of {sel_col}")
        st.plotly_chart(fig,use_container_width=True)

    if graph_type==graph_types[3]:
        fig=px.box(df,x=sel_col,title=f"Box plot of {sel_col}")
        st.plotly_chart(fig,use_container_width=True)

    if graph_type==graph_types[4]:
        fig=px.violin(df,x=sel_col,title=f"Violin plot of {sel_col}")
        st.plotly_chart(fig,use_container_width=True)






