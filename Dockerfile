FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Install dependecies for unsloth environment
# Install git and other dependencies
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.unsloth.txt .
RUN pip install --no-cache-dir -r requirements.unsloth.txt
RUN pip install --no-cache-dir -q -U google-genai
# Expose FastAPI port
EXPOSE 8000

# Start the app
CMD ["uvicorn", "src.api.main:app", "--reload", "--reload-exclude", "**/unsloth_compiled_cache/**", "--host", "0.0.0.0", "--port", "8000"]
