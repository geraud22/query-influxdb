# Use the official Python image from Docker Hub
FROM python:alpine

# Update the package lists
RUN apk update && \
    apk upgrade

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the network
EXPOSE 5000

# Set the FLASK_APP environment variable
ENV FLASK_APP=query_influxdb.py

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]