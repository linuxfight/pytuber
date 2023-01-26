import asyncio


async def download(video_url, download_type, path):
    command = f'yt-dlp -f {download_type}+bestaudio/best --merge-output-format mp4 -o {path} {video_url} --quiet'

    if download_type == 'audio':
        command = f'yt-dlp -f ba -x --audio-format m4a -o {path} {video_url} --quiet'

    process = await asyncio.create_subprocess_shell(
        command
    )

    await process.communicate()

    return path