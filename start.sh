#!/bin/bash
# Start the FastAPI backend in the background
uvicorn main:app --host 0.0.0.0 --port 8000 &
# Start the Streamlit frontend
streamlit run dashboard.py --server.port 7860 --server.address 0.0.0.0