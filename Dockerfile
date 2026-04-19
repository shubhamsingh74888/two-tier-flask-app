FROM python:3.9-slim AS builder
WORKDIR /app
RUN apt-get update \ 
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
COPY . .

FROM python:3.9-slim
WORKDIR /app
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000
ENTRYPOINT ["python","app.py"]
