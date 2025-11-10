# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files into the container
COPY . .
# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#expose flask port
EXPOSE 5000

# Set environment variables (optional)
ENV TZ=Africa/Nairobi

# Run your script
CMD ["python", "./app/live_fetch_predict.py"]
