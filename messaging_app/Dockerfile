FROM python:3.10

WORKDIR /messaging_app

COPY  requirements.txt ./

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --default-timeout=120 --retries=5 -r requirements.txt

COPY . .

CMD [ "python3", "manage.py", "runserver" ]

EXPOSE 8000