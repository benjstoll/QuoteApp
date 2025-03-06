# Use an official Python image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker caching
COPY QuoteApp/requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire QuoteApp directory into the container
COPY QuoteApp /app

# Expose the port Gunicorn will run on
EXPOSE 8000

# Run Gunicorn
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "quote:app"]