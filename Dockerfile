# Use Python as the base image
FROM python:3.9-slim

# Install system dependencies for video/audio processing and other necessary packages
RUN apt-get update && \
    apt-get install -y ffmpeg git libsndfile1 libpulse0 && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Clone the repository into the container
RUN git clone https://github.com/hema1304/Video-Voice-Over.git /app

# Navigate to the cloned directory (if needed)
WORKDIR /app

# Install Python dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask to listen on
EXPOSE 80

# Set environment variable for Flask
ENV FLASK_APP=app.py

# Set Flask to run in production mode
ENV FLASK_ENV=production

# Run the Flask application on host 0.0.0.0 and port 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
