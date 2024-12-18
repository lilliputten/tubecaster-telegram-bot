ffmpeg -i tests/test-audios/test-short.mp3  -vn -acodec pcm_s16le -ac 1 -ar 44100 -f wav tests/test-audios/test-short.converted.wav
