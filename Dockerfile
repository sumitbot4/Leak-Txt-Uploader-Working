FROM python:3.12-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies including CA certificates for SSL
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
       build-essential \
       python3-dev \
       gcc \
       libffi-dev \
       ffmpeg \
       aria2 \
       python3-pip \
       ca-certificates \
       curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app/
WORKDIR /app/

# Upgrade pip and install Python dependencies
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python3", "modules/main.py"]
