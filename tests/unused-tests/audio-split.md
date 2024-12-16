## Librosa

A test for audio files splitting, using librosa

It uses soundfile, audioread and ffmpeg.

Ffmpeg library hould be installed manually in the system, see https://www.ffmpeg.org/download.html).

See stack overflow topic [Good choice might be librosa...](https://stackoverflow.com/a/77545091/28090454) for the source of the initial idea.

Using streams:

- [librosa blog – Streaming for large files](https://librosa.org/blog/2019/07/29/stream-processing/)
- [Generators - Python Wiki](https://wiki.python.org/moin/Generators)

### Extra information

Using librosa with streams:

- [Audio Processing — Librosa Split on Silence](https://medium.com/@vvk.victory/audio-processing-librosa-split-on-silence-8e1edab07bbb)

## Other approaches:

### SoX

- [Using pysox](https://github.com/librosa/librosa/issues/897#issuecomment-498720341)

SoX on ubuntu (~2MB?):

- [marl/pysox: Python wrapper around sox.](https://github.com/marl/pysox)
- [Sox, play your MP3 files from the Ubuntu terminal](https://en.ubunlog.com/sox-plays-mp3-terminal/)
- [SoX - Sound eXchange download | SourceForge.net](https://sourceforge.net/projects/sox/)

```bash
$ sudo apt install sox libsox-fmt-all
After this operation, 1,764 kB of additional disk space will be used.
Do you want to continue? [Y/n]
```
