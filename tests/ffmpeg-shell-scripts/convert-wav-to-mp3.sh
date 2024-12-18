# ffmpeg -formats | grep mp3
# ffmpeg -i tests/test-audios/StarWars3.wav -vn -acodec pcm_s16le -ac 1 -ar 44100 -f mp3 tests/test-audios/StarWars3.converted.mp3
ffmpeg -i tests/test-audios/StarWars3.wav -vn -ar 44100 -ac 2 -b:a 192k tests/test-audios/StarWars3.converted.mp3
