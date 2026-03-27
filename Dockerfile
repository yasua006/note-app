FROM debian:stable-slim

COPY package.json package-lock.json ./

RUN apt update && apt upgrade \
&& apt install -y libmariadb-dev libmariadb3 \
&& apt install -y nodejs npm \
&& npm ci --no-audit --no-fund --verbose \
&& pip install -r requirements.txt

WORKDIR /app

COPY . /app/