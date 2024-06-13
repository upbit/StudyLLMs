> pip3 install streamlit-pdf-viewer

```py
import os
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

st.set_page_config(layout="wide")

pages = [1,2,3]
col1, col2 = st.columns([1, 1])
with col1:
    pdf_viewer("2302.02676v8.pdf", pages_to_render=pages, key="p1")
with col2:
    pdf_viewer("2302.02676v8.pdf", pages_to_render=pages, key="p2")
```

标记例子：[lfoppiano/structure-vision](https://github.com/lfoppiano/structure-vision)
