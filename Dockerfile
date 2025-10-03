# Use a modern Python base
FROM python:3.12-slim-bookworm

# Set environment variables for non-interactive apt
ENV DEBIAN_FRONTEND=noninteractive

# Update and install required packages
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends gcc libffi-dev ffmpeg aria2 python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app/
WORKDIR /app/

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Set default command to start the bot
CMD ["python3", "modules/main.py"]
