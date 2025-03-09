# Use an official Python image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker caching
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire QuoteApp directory into the container
COPY QuoteApp /app/QuoteApp
COPY gemini_handler /app/gemini_handler
COPY dynamo_handler /app/dynamo_handler

# Expose the port Gunicorn will run on
EXPOSE 8000

# Run Gunicorn
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "QuoteApp:create_app()"]