# Use a Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server files
COPY . .

# Expose the port the server runs on (change if necessary)
EXPOSE 50051

# Command to run the server
CMD ["python", "Server.py"]
