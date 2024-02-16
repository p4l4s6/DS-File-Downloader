FROM python:3.11-slim-buster

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . /app

# Create the SQLite database (if needed)
WORKDIR app/

# Expose app port
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "main:app"]
