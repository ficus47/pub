import streamlit as st
import streamlit.components.v1 as components

adsense_code = """
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8075907034534804"
     crossorigin="anonymous"></script>
"""

components.html(adsense_code, height=100)
