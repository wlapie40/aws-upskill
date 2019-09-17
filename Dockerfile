FROM python:3.6

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt&&mkdir /root/.aws

VOLUME /root/.aws/

ARG FLASK_APP=app.py

EXPOSE 5000

CMD ["python","app.py"]

