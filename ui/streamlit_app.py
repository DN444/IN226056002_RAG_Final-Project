import streamlit as st
import requests
import uuid

st.title("RAG Customer Support Assistant")

# Session ID for memory
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

query = st.text_input("Ask your question:")

if st.button("Submit") and query:
    response = requests.post(
        "http://127.0.0.1:8000/query_stream",
        json={
            "query": query,
            "session_id": st.session_state.session_id
        },
        stream=True
    )

    output = ""
    placeholder = st.empty()

    for chunk in response.iter_content(chunk_size=10):
        if chunk:
            output += chunk.decode()
            placeholder.markdown(output)

    st.success("Done")