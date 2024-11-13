# Use a lightweight base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements1.txt .

# Update and install necessary system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    portaudio19-dev \
    libasound2-dev \
    libjack-jackd2-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --ignore-installed -r requirements1.txt

# Copy the rest of the application files
COPY . .

# Set environment variables for Flask-Mail (replace with actual credentials)
ENV MAIL_SERVER="smtp.gmail.com" \
    MAIL_PORT=465 \
    MAIL_USERNAME="videovoiceover2023@gmail.com" \
    MAIL_PASSWORD="qzvq wito zrvo khmk" \
    MAIL_USE_TLS="False" \
    MAIL_USE_SSL="True" 

# Expose the port the app runs on
EXPOSE 80

# # Start the application
# CMD ["python", "app.py"]

CMD ["bash", "start.bat"]

