FROM python:3.11-alpine
WORKDIR /app

RUN apk add yt-dlp ffmpeg
COPY utils/* ./utils
COPY .env .
COPY requirements.txt .
COPY main.py .

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN pip install -r requirements.txt

CMD ["python", "main.py"]