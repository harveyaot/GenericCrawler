FROM python:3.11.1-slim-bullseye
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD cd opinionnews && scrapy crawl newsweek
