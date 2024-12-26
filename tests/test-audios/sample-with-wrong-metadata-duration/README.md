# The wrong metadata duration problem

NOTE: The duration value returned by ffmepg's probe (see beloq) from the metadta could be incorrect.

According to a stack overflow' solution there is a way to determine a correct duration via ffprobe:

Link: [linux - How does ffprobe determine duration? - Stack Overflow](https://stackoverflow.com/questions/30582452/how-does-ffprobe-determine-duration)

One simple solution is to use `-show_packets` option

```bash
$ ffprobe -i file.mp3  -show_entries format=duration -v quiet -of csv="p=0"
160.701514 # Wrong duration
$ ffprobe -i file.mp3 -show_packets > result.txt
$ grep dts_time result.txt
...
dts_time=167.183673 # Correct duration
```

Now open a result file and go to the last packet and see `dts_time` value
that would be the accurate duration of file. If `dts_time` is not defined
check for the `pts_time` value.

