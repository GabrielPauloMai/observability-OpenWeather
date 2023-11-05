FROM python:3.8-slim

LABEL description="Dockerfile"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip3 install --upgrade pip \
    && pip3 install -r requirements

EXPOSE 5000

CMD ["python", "web.py"]
