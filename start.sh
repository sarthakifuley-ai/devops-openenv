#!/bin/bash
# Start FastAPI from the new location in the background
uvicorn server.app:app --host 0.0.0.0 --port 8000 &

# Start Streamlit 
streamlit run dashboard.py --server.port 7860 --server.address 0.0.0.0