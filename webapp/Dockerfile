#Dockerfile for Flask app
FROM python:3.8

# Set working directory
WORKDIR /usr/src/app

# Copy project files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=run.py

# Run app.py when the container launches
#CMD ["flask", "run", "--host=0.0.0.0"]
