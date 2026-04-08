# Use python-slim for a smaller footprint
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
# Note: Ensure "openenv-core>=0.2.0" is added to your requirements.txt!
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir openenv-core>=0.2.0

# Copy everything (including the new /server folder)
COPY . .

# Expose the ports for both FastAPI (8000) and Streamlit (7860/8501)
EXPOSE 8000
EXPOSE 7860

# Ensure start.sh is executable
RUN chmod +x start.sh

# Run the start script
CMD ["sh", "start.sh"]