FROM python:3.11-slim-buster

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . /app

# Create the SQLite database (if needed)
WORKDIR app/

# Expose app port
EXPOSE 9000

# Start the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
