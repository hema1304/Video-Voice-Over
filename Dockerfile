# Use an official Python 3.10 image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy application files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --ignore-installed -r requirements_linux.txt

# Set environment variables for Flask-Mail
ENV MAIL_SERVER=smtp.gmail.com \
    MAIL_PORT=465 \
    MAIL_USERNAME=videovoiceover2023@gmail.com \
    MAIL_PASSWORD='qzvq wito zrvo khmk' \
    MAIL_USE_TLS=False \
    MAIL_USE_SSL=True

# Expose port 80
EXPOSE 80

# Run the Flask app
CMD ["python", "app.py"]

