# Youtube download libraries
# import youtube_dl # @see https://github.com/ytdl-org/youtube-dl
import yt_dlp  # @see https://github.com/yt-dlp/yt-dlp

YTDL = yt_dlp

logTraceback = False

# Eg:
# https://www.youtube.com/watch?v=EngW7tLk6R8
# /cast https://www.youtube.com/watch?v=EngW7tLk6R8
# /info https://www.youtube.com/watch?v=EngW7tLk6R8

# demoVideo = 'https://youtu.be/Mq_x4Nown2o?si=7kqgsHkP-wO4PKdu'  # Causes the error: Mq_x4Nown2o: Requested format is not available. Use --list-formats for a list of available formats
# demoVideo = 'https://www.youtube.com/watch?v=EngW7tLk6R8'  # Short video, 00:05
demoVideo = 'https://youtu.be/N02Y7vaVDNo?si=xwgKLdqfcWvKyBjv'  # Audio test (produces 'The downloaded file is empty' error)
#  demoVideo = 'https://www.youtube.com/watch?v=UdaQRvVTIqU'   # Video with a russian title, 02:47
#  demoVideo = 'https://www.youtube.com/watch?v=eBHLST0pLXg'   # Video with a russian title, 00:18
#  # Last video with a playlist
#  demoVideo = 'https://www.youtube.com/watch?v=eBHLST0pLXg&list=PLuDoUpt1iJ4XHDwHJm7xjFLiYJXTf4ouv&index=3'


__all__ = [
    'YTDL',
    'logTraceback',
    'demoVideo',
]
