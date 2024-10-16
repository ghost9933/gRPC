# Dockerfile for Pet Adoption gRPC Server
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project files
COPY . .

# Run the server
CMD ["python", "Server/Server.py"]
