from mutagen.mp4 import MP4, MP4Cover


def set_artist(path, artist):
    file = MP4(path)
    file.tags['\xa9ART'] = artist
    file.save(path)
    
    
def set_title(path, title):
    file = MP4(path)
    file.tags['\xa9nam'] = title
    file.save(path)


def set_cover(path, cover):
    file = MP4(path)
    with open(cover, 'rb') as f:
        albumart = MP4Cover(f.read())
    file.tags['covr'] = [albumart]
    file.save(path)