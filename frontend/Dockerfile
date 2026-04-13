# Dockerfile for the Streamlit frontend
#
# Same idea as the API Dockerfile:
# Start from Python, install dependencies, copy code, run.

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8501

# Streamlit-specific flags:
# --server.headless=true    : don't try to open a browser (there's no browser inside a container)
# --server.address=0.0.0.0  : listen on all interfaces (so Docker can route traffic to it)
CMD ["streamlit", "run", "app.py", "--server.headless=true", "--server.address=0.0.0.0", "--server.port=8501"]
