# Use the official Python image as the base image
FROM python:3.11

# Set an environment variable to avoid buffering of Python output
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /hrms-automation

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
