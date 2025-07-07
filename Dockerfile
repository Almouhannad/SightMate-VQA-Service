FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Install dependecies for unsloth environment
COPY requirements.unsloth.txt .
RUN pip install --no-cache-dir -r requirements.unsloth.txt

# Expose FastAPI port
EXPOSE 8000

# Start the app
CMD ["uvicorn", "src.api.main:app", "--reload", "--reload-exclude", "**/unsloth_compiled_cache/**", "--host", "0.0.0.0", "--port", "8000"]
