# import streamlit as st
# from query_engine import ask_question

# st.title("🚗 Car Manual RAG Bot")

# query = st.text_input("Ask about the car manual")

# if query:

#     result = ask_question(query)

#     st.write(result["text"])

#     if result["image_path"]:
#         st.image(result["image_path"])


import streamlit as st
from query_engine import ask_question

st.title("🚗 Car Manual Multimodal RAG Bot")

query = st.text_input("Ask about the car manual")

if query:

    result = ask_question(query)

    st.write(result["text"])

    for img in result["images"]:
        st.image(img)