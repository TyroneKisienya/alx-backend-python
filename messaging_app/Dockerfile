FROM python:3.10

WORKDIR /messaging_app

COPY  requirements.txt ./

RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --default-timeout=120 --retries=5 -r requirements.txt

COPY . .

CMD [ "python3", "manage.py", "runserver" ]

EXPOSE 8000