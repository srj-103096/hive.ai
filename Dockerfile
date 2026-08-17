FROM python:3.12-alpine

WORKDIR /app

COPY scraper.py .

EXPOSE 9100

CMD ["python3", "scraper.py"]
