# ffprobe tests/test-audios/test-short.mp3 > tests/test-audios/test-short.probe.txt 2>&1 && car tests/test-audios/test-short.probe.txt

# Get duration:
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 tests/test-audios/test-short.mp3

# Get all data in json:
# ffprobe -hide_banner -loglevel fatal -show_error -show_format -print_format json tests/test-audios/test-short.mp3
ffprobe -hide_banner -loglevel fatal -show_error -show_entries stream=codec_name,duration -show_format -print_format json tests/test-audios/test-short.mp3

# Full output
ffprobe -show_format -show_streams -of json tests/test-audios/test-short.mp3

# Output example:
#
# {
#     "programs": [
#
#     ],
#     "stream_groups": [
#
#     ],
#     "streams": [
#         {
#             "codec_name": "aac",
#             "duration": "5.433469"
#         }
#     ],
#     "format": {
#         "filename": "test-audios/test-short.mp3",
#         "nb_streams": 1,
#         "nb_programs": 0,
#         "nb_stream_groups": 0,
#         "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
#         "format_long_name": "QuickTime / MOV",
#         "start_time": "0.000000",
#         "duration": "5.433469",
#         "size": "22551",
#         "bit_rate": "33203",
#         "probe_score": 100,
#         "tags": {
#             "major_brand": "dash",
#             "minor_version": "0",
#             "compatible_brands": "iso6mp41",
#             "creation_time": "2024-06-25T22:41:23.000000Z",
#             "encoder": "Google"
#         }
#     }
# }
