import re
import os

# Youtube download libraries
# import youtube_dl # @see https://github.com/ytdl-org/youtube-dl
import yt_dlp   # @see https://github.com/yt-dlp/yt-dlp


YTDL = yt_dlp


def getFileIdFromName(name: str):
    filename = name.lower()
    filename = re.sub(r'\W+', ' ', filename).strip()
    filename = re.sub(r'\s+', '-', filename)
    return filename


def run():
    url = 'https://www.youtube.com/watch?v=EngW7tLk6R8'
    #  url = input("please enter youtube video url:")
    video_info = YTDL.YoutubeDL().extract_info(url=url, download=False)
    if not video_info:
        raise Exception('No video info has been returned')
    title = video_info['title']
    webpage_url = video_info['webpage_url']
    fileid = getFileIdFromName(title)
    filename = 'temp-' + fileid + '.mp3'
    cwd = os.getcwd()
    filepath = os.path.join(cwd, filename)
    print('filepath: %s' % filepath)
    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filepath,
    }

    with YTDL.YoutubeDL(options) as ydl:
        ydl.download([webpage_url])

    print('Download complete...')


if __name__ == '__main__':
    run()
