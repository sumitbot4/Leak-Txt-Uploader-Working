FROM python:3.12-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# Install required system packages
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
       build-essential \
       python3-dev \
       gcc \
       libffi-dev \
       libssl-dev \
       ca-certificates \
       ffmpeg \
       aria2 \
       python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy app files
COPY . /app/
WORKDIR /app/

# Upgrade pip and install dependencies
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --no-cache-dir -r requirements.txt

# Start the bot
CMD ["python3", "modules/main.py"]
