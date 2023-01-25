FROM python:3.11-alpine
WORKDIR /app

RUN apk add yt-dlp
COPY app ./app
COPY .env ./app

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN pip install -r app/requirements.txt

CMD ["python", "app/main.py"]