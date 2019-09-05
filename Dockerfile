FROM python:3.6

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt&& \
    mkdir /root/.aws

VOLUME /root/.aws/

EXPOSE 5000

ENV FLASK_ENV=docker

CMD ["python", "app.py"]