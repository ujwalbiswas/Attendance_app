import streamlit as st
import Face_rec


st.set_page_config(page_title='Attendance System',layout='wide')

st.header('Attendance System Using Face Recogination')

with st.spinner("Loading Mdels and Connecting to radis db ..."):

 st.success('Model loads sucesfully')
 st.success('Redis db sucessfully connected')