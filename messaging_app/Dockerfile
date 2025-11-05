FROM python:3.10

WORKDIR /home/skai/Desktop/alx-backend-python/messaging_app

COPY  requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "manage.py", "runserver" ]

EXPOSE 8000