import os

print("Starting FastAPI...")
os.system("uvicorn app.main:app --reload")

print("Starting Streamlit...")
os.system("streamlit run ui/streamlit_app.py")