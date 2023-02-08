# pytuber
Telegram bot for downloading videos from youtube.

You need telegram api_hash and api_id to host bot.
Create ```.env``` file in bot directory, ```.env``` should look like:
```
API_ID=YOURAPIID
API_HASH=YOURAPIHASH
BOT_TOKEN=YOURBOTTOKEN
```

Then ```docker build -t pytuber .``` and ```docker run -d --restart unless-stopped pytuber```
