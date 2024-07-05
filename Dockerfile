# docker pull python
FROM python:3.10.14-alpine3.20

RUN adduser -g "noroot" -D noroot

WORKDIR /fastAPI-app
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod 755 /fastAPI-app

COPY ./app/. .

USER noroot

CMD ["python", "main.py"]
