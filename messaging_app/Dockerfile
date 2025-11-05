FROM python:3.10

WORKDIR /messaging_app

COPY  requirements.txt ./

RUN apt-get update && apt-get install -y \
    build-essential \
    libmysqlclient-dev \
    pkg-config \
    python3-dev \
    libcairo2-dev \
    libgirepository1.0-dev \
    gir1.2-gtk-3.0 \
    libdbus-1-dev \
    libdbus-glib-1-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --default-timeout=120 --retries=5 -r requirements.txt

COPY . .

CMD [ "python3", "manage.py", "runserver" ]

EXPOSE 8000