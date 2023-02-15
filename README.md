# pytuber
Telegram bot for downloading videos from youtube.

You need telegram api_hash and api_id to host bot.
Create ```docker-compose.yaml``` in new directory:
```
version: "1.0"

services:
    pytuber:
      container_name: pytuber
      image: linuxfight/pytuber:latest
      environment:
            - BOT_TOKEN=BOT_TOKEN
            - API_HASH=API_HASH
            - API_ID=API_ID
      volumes:
            - ".:/app"
      restart: unless-stopped
```

Run ```docker compose up``` or ```docker-compose up -d``` and you are ready to go.
