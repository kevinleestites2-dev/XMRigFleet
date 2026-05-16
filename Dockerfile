FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y wget curl python3 python3-pip && rm -rf /var/lib/apt/lists/*

RUN wget -q https://github.com/xmrig/xmrig/releases/download/v6.22.2/xmrig-6.22.2-linux-static-x64.tar.gz     && tar -xzf xmrig-6.22.2-linux-static-x64.tar.gz     && mv xmrig-6.22.2/xmrig /usr/local/bin/xmrig     && chmod +x /usr/local/bin/xmrig     && rm -rf xmrig-6.22.2*

WORKDIR /app
COPY . .
RUN pip3 install --no-cache-dir requests

CMD ["python3", "-u", "miner.py"]
