import os
import pathlib
import posixpath
import re
import traceback

# Youtube download libraries
# import youtube_dl # @see https://github.com/ytdl-org/youtube-dl
import yt_dlp  # @see https://github.com/yt-dlp/yt-dlp

YTDL = yt_dlp

from botCast.config.castConfig import demoVideo, logTraceback


def getFileIdFromName(name: str):
    filename = name.lower()
    filename = re.sub(r'\W+', ' ', filename).strip()
    filename = re.sub(r'\s+', '-', filename)
    return filename


def run():
    # url = 'https://www.youtube.com/watch?v=EngW7tLk6R8' # Mini test
    # url = 'https://www.youtube.com/watch?v=VgyQ-1tzFaY'   # Autodubbed test
    url = demoVideo
    try:
        #  url = input("please enter youtube video url:")
        ytdl = YTDL.YoutubeDL()
        video_info = ytdl.extract_info(url=url, download=False)
        if not video_info:
            raise Exception('No video info has been returned')
        title = video_info['title']
        webpage_url = video_info['webpage_url']
        fileid = getFileIdFromName(title)
        # filename = 'temp-' + fileid + '.mp3'
        filename = 'temp.mp3'
        cwd = pathlib.Path(os.getcwd()).as_posix()
        filepath = posixpath.join(cwd, filename)
        print('run: filepath: %s' % filepath)
        options = {
            # 'format': 'bestaudio/best',
            'format': 'worstaudio/worst',
            'keepvideo': False,
            'outtmpl': filepath,
        }

        with YTDL.YoutubeDL(options) as ydl:
            ydl.download([webpage_url])

        print('run: Download complete')
    except Exception as err:
        errText = repr(err)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Video test error: ' + errText
        print('run: Traceback for the following error:' + sTraceback)
        print('run: ' + errMsg)
        raise Exception(errMsg)


if __name__ == '__main__':
    run()
