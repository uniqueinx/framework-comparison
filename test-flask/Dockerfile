FROM python:3.9-slim
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
RUN pip install -r requirements.txt
ADD . /app

ENTRYPOINT ["/app/entrypoint.sh"]
