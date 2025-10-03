FROM python:3.12-slim-bookworm
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
       build-essential \
       python3-dev \
       gcc \
       libffi-dev \
       libssl-dev \
       ffmpeg \
       aria2 \
       python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/

RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "modules/main.py"]
