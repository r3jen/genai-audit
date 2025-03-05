# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PORT=8080

# Make port 8080 available
EXPOSE 8080

# Command to run the application
CMD streamlit run --server.port $PORT --server.address 0.0.0.0 app.py