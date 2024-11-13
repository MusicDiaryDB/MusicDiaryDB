# Use the official Python 3.12 image from Docker Hub
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Installing core dependencies
RUN apt-get update && apt-get install -y libpq-dev build-essential


# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Expose the port the app runs on (adjust if necessary)
EXPOSE 5400

# populate database with sample data
RUN python scripts/setup.py

# Command to run the application
CMD ["python", "main.py"]
