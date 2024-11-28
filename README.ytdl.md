<!--
 @since 2024.11.27, 14:56
 @changed 2024.11.27, 15:09
-->


# Youtube downloader library notes

## yt-dlp

- See [yt-dlp/yt-dlp: A feature-rich command-line audio/video downloader](https://github.com/yt-dlp/yt-dlp)

Finally decided to use yt-dlp. But it turned out that it's not possible to deal with saving files on vercel -- the library just silently fails during the downloading process.


## youtube-dl (UNUSED)

By default install we get an error:

```
ERROR: Unable to extract uploader id; please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output.
```

See discussion:

- [python - Error: Unable to extract uploader id - Youtube, Discord.py - Stack Overflow](https://stackoverflow.com/questions/75495800/error-unable-to-extract-uploader-id-youtube-discord-py)

So, it's required to use github master installation:

```
poetry add git+https://github.com/ytdl-org/youtube-dl.git@master
```

Or, for pip (to use for tests in command line, it it's required):

```
pip install --force-reinstall https://github.com/ytdl-org/youtube-dl/archive/master.tar.gz
...
Successfully installed youtube_dl-2021.12.17
```

Youtube cookies are required to allow cope with 'Sign in to confirm...' error.

Could be jsut copied form any logged-in browser and stored in `YT_COOKIE` environment variable. Don't forget about the first line (`# Netscape HTTP Cookie File`). Empty lines are allowed.



