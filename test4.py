import streamlit as st
import pdf_engineering.table_pdf_to_img as pdf_engineering
import time
from streamlit_js_eval import streamlit_js_eval

# logtxtbox = st.empty()
# logtxt = 'start'
# logtxtbox.text(body="First text")

# for i in range (100):
#     logtxtbox.text(body=str(i))
#     time.sleep(0.2)

# logtxtbox.empty()

st.text_input(label="Input your value here...")

st.balloons()


# time.sleep(20)

if st.button("Reload page"):
    streamlit_js_eval(js_expressions="parent.window.location.reload()")
