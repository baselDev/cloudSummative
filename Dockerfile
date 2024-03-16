# Use the official Python image as a base image
FROM python:3.10.6

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose the port that your app runs on
EXPOSE 5000/tcp

# Command to run the application
CMD ["python", "./app.py"]
