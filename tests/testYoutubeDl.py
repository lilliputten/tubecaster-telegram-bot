import youtube_dl
import re


def run():
    video_url = 'https://www.youtube.com/watch?v=EngW7tLk6R8'
    #  video_url = input("please enter youtube video url:")
    video_info = youtube_dl.YoutubeDL().extract_info(url=video_url, download=False)
    if not video_info:
        raise Exception('No video info has been returned')
    title = video_info['title']
    webpage_url = video_info['webpage_url']
    filename = title.lower()
    filename = re.sub(r'\W+', ' ', filename).strip()
    filename = re.sub(r'\s+', '-', filename)
    filename = 'out/' + filename + '.mp3'
    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([webpage_url])

    print('Download complete... {}'.format(filename))


if __name__ == '__main__':
    run()
