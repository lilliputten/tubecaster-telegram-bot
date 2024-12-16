# ffmpeg -i tests/test-audios/StarWars3.wav -f segment -segment_time 1 -c copy out/split-%03d.mp3
# ffmpeg -i tests/test-audios/test-short.mp4 -vn -f segment -segment_time 3 -c copy out/split-%09d.mp4
ffmpeg -i tests/test-audios/test-short -vn -acodec copy -ss 0 -to 2.5 -f mp4 out/piece.mp4
ffmpeg -i tests/test-audios/test-short.mp4 -vn -acodec copy -ss 0 -to 2.5 out/piece.mp4
