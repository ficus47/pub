import streamlit as st
import streamlit.components.v1 as components
import os

# Fonction pour injecter le code HTML dans la balise <head>
def inject_html_in_head():
    custom_head = """
    <head>
    <title>Custom Streamlit App</title>
    <meta name="google-adsense-account" content="ca-pub-8075907034534804">
    <style>
        body {
            background-color: lightgrey;
        }
    </style>
    </head>
    """
    components.html(custom_head, height=0)

st.write(os.listdir())
st.write("click ! ")

st.write(os.listdir(os.listdir()[1]))
st.write(os.listdir(os.listdir()[2]))

st.write(os.listdir(os.listdir()[2]+"/HEAD"))
