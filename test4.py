import streamlit as st
import pdf_engineering.table_pdf_to_img as pdf_engineering
import time

logtxtbox = st.empty()
logtxt = 'start'
logtxtbox.text(body="First text")

for i in range (100):
    logtxtbox.text(body=str(i))
    time.sleep(0.2)

logtxtbox.empty()
