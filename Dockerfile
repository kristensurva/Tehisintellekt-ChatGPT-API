# Use official Python 3.10 slim image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the local requirements file to the container
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Default command to run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]