FROM python:3.10

WORKDIR /code/

RUN apt-get update && apt-get install libpq-dev python3-dev -y

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . /code/

EXPOSE 8000