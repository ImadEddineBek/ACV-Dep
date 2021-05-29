FROM python:3.8-slim

ENV APP_FOLDER="/app/src"

RUN apt-get update && apt-get install -y git gcc zip

COPY requirements.txt .
RUN pip install --upgrade -r requirements.txt --no-cache-dir && rm requirements.txt

COPY src/*.py $APP_FOLDER/

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=$APP_FOLDER
WORKDIR /

ENTRYPOINT ["python", "/app/src/main.py"]
