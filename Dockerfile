FROM python:alpine3.17

WORKDIR /app
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
RUN python -m venv /venv

COPY src/ .
RUN apk add yt-dlp ffmpeg
RUN pip install -r requirements.txt
RUN apk update && apk upgrade

CMD ["python", "src/main.py"]