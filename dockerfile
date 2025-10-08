# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (optional)
ENV TZ=Africa/Nairobi

# Run your script
CMD ["python", "live_fetch_predict.py"]

FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Install cron
RUN apt-get update && apt-get install -y cron

# Add cron job: 9AM and 5PM EAT (6AM and 2PM UTC)
RUN echo "0 6,14 * * * python /app/live_fetch_predict.py >> /app/logs.txt 2>&1" > /etc/cron.d/weather-cron
RUN chmod 0644 /etc/cron.d/weather-cron && crontab /etc/cron.d/weather-cron

# Start cron in the foreground
CMD cron -f
