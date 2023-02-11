import yt_dlp

from tempfile import TemporaryDirectory
from pathlib import Path
from pyrogram import enums, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from utils.storage import save, load
from utils.download import download
from utils.thumbnail import get_thumbnail
from utils.edit_metadata import set_cover, set_artist, set_title

video_formats = ['135', '136', '298', '137', '299', '400', '401']
low_res = ['160', '133', '134']
storage: dict = load()


def resolution_keyboard(video_id):
    buttons = []

    with yt_dlp.YoutubeDL() as ydl:
        info: dict = ydl.extract_info(
            download=False,
            url=f'https://youtu.be/{video_id}'
        )

    formats: list[dict] = info['formats']
    audio_formats = []

    for f in formats:
        if f['resolution'] == 'audio only':
            audio_formats.append(f)
        if f['format_id'] in video_formats:
            if f.get('filesize'):
                file_size = int(f.get('filesize') / (1024 * 1024))
            else:
                file_size = int(f.get('filesize_approx') / (1024 * 1024))
            file_size += int(audio_formats[-1]['filesize'] / (1024 * 1024))
            itag = f['format_id']
            if file_size <= 2000:
                buttons.append([
                        InlineKeyboardButton(
                            text=str(f['resolution']) + 'p ' + str(f['fps']) + 'fps ' + str(file_size) + 'MB',
                            callback_data=f'{video_id}:{itag}'
                        )
                    ])

    if buttons == []:
        for f in formats:
            if f['format_id'] in low_res:
                if f.get('filesize'):
                    file_size = int(f.get('filesize') / (1024 * 1024))
                else:
                    file_sizs = int(f.get('filesize_approx') / (1024 * 1024))
                file_size += int(audio_formats[-1]['filesize'] / (1024 * 1024))
                itag = f['format_id']
                if file_size <= 2000:
                    buttons.append([
                            InlineKeyboardButton(
                                text=str(f['resolution']) + 'p ' + str(f['fps']) + 'fps ' + str(file_size) + 'MB',
                                callback_data=f'{video_id}:{itag}'
                            )
                        ])
    return InlineKeyboardMarkup(
        buttons
    )


async def on_callback_query(client: Client, callback_query: CallbackQuery):
    data = callback_query.data.split(':')
    video_id = data[0]
    download_type = data[1]
    ext = 'mp4'

    if download_type == 'audio':
        ext = 'm4a'
    else:
        if download_type == 'video':
            await client.send_message(
                chat_id=callback_query.message.chat.id,
                reply_to_message_id=callback_query.message.id,
                text='Выберите разрешение видео',
                reply_markup=resolution_keyboard(video_id)
            )
            return

    save_path = f'{video_id}:{download_type}'
    item = storage.get(save_path)

    if item == 'Working':
        await callback_query.answer(
            text='⚙ Производится скачивание, пожалуйста подождите'
        )
        return
    if item is None:
        storage.update({save_path: 'Working'})
    await callback_query.answer(
        text='⚙ Обработка запроса'
    )
    await save(storage)

    if item != 'Working' and item is not None:
        file = item
        if download_type == 'audio':
            await client.send_chat_action(
                chat_id=callback_query.message.chat.id,
                action=enums.ChatAction.UPLOAD_AUDIO
            )
            await client.send_audio(
                chat_id=callback_query.message.chat.id,
                reply_to_message_id=callback_query.message.id,
                audio=file
            )
            return
        await client.send_chat_action(
            chat_id=callback_query.message.chat.id,
            action=enums.ChatAction.UPLOAD_VIDEO
        )
        await client.send_video(
            chat_id=callback_query.message.chat.id,
            reply_to_message_id=callback_query.message.id,
            video=file
        )
        return


    with TemporaryDirectory() as temp:
        with yt_dlp.YoutubeDL() as ydl:
            info: dict = ydl.extract_info(
                download=False,
                url=f'https://youtu.be/{video_id}'
            )

            title = info['title']
            channel = info['channel']
            duration = int(info['duration'])
            thumbnails = info['thumbnails']
            thumb = await get_thumbnail(thumbnails[-1]['url'], f'{Path(temp)}/thumb.jpg')

        height = 0
        width = 0
        if download_type.isdigit():
            for f in info['formats']:
                if str(f['format_id']) == download_type:
                    width = f['width']
                    height = f['height']
        path = await download(f'https://youtu.be/{video_id}', download_type, f'{Path(temp)}/{video_id}.{ext}')
        set_cover(path, thumb)
        set_title(path, title)
        set_artist(path, channel)
        file = None
        if download_type == 'audio':
            await client.send_chat_action(
                chat_id=callback_query.message.chat.id,
                action=enums.ChatAction.UPLOAD_AUDIO
            )
            file = await client.send_audio(
                chat_id=callback_query.message.chat.id,
                reply_to_message_id=callback_query.message.id,
                audio=path,
                thumb=thumb,
                duration=duration,
                performer=channel,
                title=title
            )
        else:
            await client.send_chat_action(
                chat_id=callback_query.message.chat.id,
                action=enums.ChatAction.UPLOAD_VIDEO
            )
            file = await client.send_video(
                chat_id=callback_query.message.chat.id,
                reply_to_message_id=callback_query.message.id,
                video=path,
                thumb=thumb,
                duration=duration,
                width=width,
                height=height
            )


    file_id = None
    if file.video:
        file_id = file.video.file_id
    else:
        file_id = file.audio.file_id
    storage.update({save_path: file_id})
    await save(storage)
