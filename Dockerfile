# Use a lightweight Python image as the base
FROM python:3.10-alpine

# Install dependencies for audio processing and other required libraries
RUN apk add --no-cache ffmpeg libsndfile libpulse

# Set the working directory in the container
WORKDIR /app

# Copy local application files to the container
COPY . /app

# Install Python dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements_linux.txt

# Expose port 80 for Flask
EXPOSE 80

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the Flask application on host 0.0.0.0 and port 80
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
