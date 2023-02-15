FROM python:alpine

WORKDIR /app
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
RUN python -m venv /venv

COPY src/ .
RUN apk add yt-dlp ffmpeg
RUN pip install -r requirements.txt

CMD ["python", "src/main.py"]