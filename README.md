<!--
 @since 2024.11.20, 02:55
 @changed 2024.11.20, 02:55
-->


# tubecaster-telegram-bot

Simple video to audio caster telegram bot

(TODO: Describe the main features.)


## Build info (auto-generated)

- Project info: v.0.0.6 / 2024.11.25 19:47:04 +0300


## Resources

Repository: https://github.com/lilliputten/tubecaster-telegram-bot

Vercel panel: https://vercel.com/lilliputtens-projects/tubecaster-telegram-bot-wcb6

Vercel hosted application: https://tubecaster-telegram-bot-wcb6.vercel.app/


## Deployment procedure

Initialize or deploy current state with:

```
vercel
```

Don't forget to:

1. Disable the deployment protection on the project:

```
Settings -> Deployment Protection
```

2. Connect the github repository to automate builds:

```
Settings -> Git
```


## Youtube-dl notes

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

