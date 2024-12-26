# -*- coding:utf-8 -*-

from datetime import timedelta
import pathlib
import re
import traceback
from typing import Callable

from core.logger import getDebugLogger
from core.logger.utils import errorStyle, errorTitleStyle, warningStyle, secondaryStyle, primaryStyle, titleStyle
from core.appConfig import AUDIO_FILE_EXT
from core.helpers.errors import errorToString
from core.utils import debugObj
from core.ffmpeg import probe, split


# The parameters to pass to a callback are:
# - audioFileName: str - Source audio file name (is already on the disk);
# - pieceNo: (int | None) - piece number;
# - piecesCount: int | None - Total pieces count;
TPieceCallback = Callable[[str, int | None, int | None], None]

logTraceback = False

_logger = getDebugLogger()


def splitAudio(
    audioFileName: str,
    outFilePrefix: str,
    piecesCount: int = 1,
    pieceCallback: TPieceCallback | None = None,
    delimiter: str = '-',
    gap: int = 0,
    removeFiles: bool = True,
    duration: float | None = None,
):
    """
    Split large audio file into pieces via ffmpeg (should be installed in the system).

    Parameters:

    - audioFileName: Input audio path.
    - outFilePrefix: Output file prefix. Will be extended by `{delimiter}{no}{.ext}`.
    - delimiter: A delimiter between file prefix and number parts in output file name (default value is '-').
    - piecesCount: Desired pieces count.
    - pieceCallback: Callback to process each piece, when file has already been
      written. The following parameteres will be passed: filename, piece number, total pieces count.
    - gap: Add an overlapping gap (in seconds) at the place of pieces junction. 0 to no gaps.
    - removeFiles: Automatically remove piece files when done (after callback return, if specified).
    - duration: 'True' duration (in case if yt-downloaded audio has wrong duration; probably that;s a ytdl library bug? See Issue #34).

    NOTE: The duration value returned by ffmepg's probe (see beloq) from the metadta could be incorrect.

    According to a stack overflow' solution there is a way to determine a correct duration via ffprobe:

    Link: [linux - How does ffprobe determine duration? - Stack Overflow](https://stackoverflow.com/questions/30582452/how-does-ffprobe-determine-duration)

    One simple solution is to use `-show_packets` option

    ```bash
    ffprobe -i file.mp3 -show_packets > result.txt
    ```

    Now open a result file and go to the last packet and see `dts_time` value
    that would be the accurate duration of file. If `dts_time` is not defined
    check for the `pts_time` value.
    """
    try:
        _logger.info(f'splitAudio: Start creating pieces for file: {audioFileName}')

        probeData = probe(audioFileName)

        format = probeData.get('format', {})
        audioDuration = float(format.get('duration', '0'))
        usedDuration = duration if duration else audioDuration
        pieceDurationSec = usedDuration / piecesCount

        # Show debug info
        debugItems = {
            'audioFileName': audioFileName,
            'duration': duration,
            'durationFmt': timedelta(seconds=float(duration)) if duration else None,
            'usedDuration': usedDuration,
            'usedDurationFmt': timedelta(seconds=float(usedDuration)) if usedDuration else None,
            'audioDuration': audioDuration,
            'audioDurationFmt': timedelta(seconds=float(audioDuration)) if audioDuration else None,
            'pieceDurationSec': pieceDurationSec,
            'audioDurationSecFmt': timedelta(seconds=pieceDurationSec) if pieceDurationSec else None,
            'piecesCount': piecesCount,
            'TEST': errorTitleStyle(
                'Issue #34: audioDuration should be equal videoDuration (see prev log output from sendAudioToChat)!'
            ),
        }
        logItems = [
            titleStyle('splitAudio: Audio file is going to be split'),
            secondaryStyle(debugObj(debugItems)),
        ]
        logContent = '\n'.join(logItems)
        _logger.debug(logContent)

        hasPieces = piecesCount > 1
        pieces = range(piecesCount)
        for n in pieces:
            no = n + 1
            start = n * pieceDurationSec
            if gap and n:
                start -= gap
            end = (n + 1) * pieceDurationSec
            if gap and n < piecesCount - 1:
                end += gap
            outputFileName = outFilePrefix
            if hasPieces:
                outputFileName += delimiter + str(no)
            outputFileName += AUDIO_FILE_EXT
            _logger.info(f'splitAudio: Creating piece {no}/{piecesCount} ({start}-{end}) -> {outputFileName})')
            split(audioFileName, outputFileName, start=start, end=end)
            if pieceCallback:
                pieceCallback(outputFileName, n, piecesCount)
            if removeFiles:
                pathlib.Path(outputFileName).unlink(missing_ok=True)

        _logger.info(f'splitAudio: Already created all {piecesCount} piece(s)')

    except Exception as err:
        errText = re.sub('[\n\r]+', ' ', errorToString(err, show_stacktrace=False))
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Audio splitting error: ' + errText
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle('splitAudio: Traceback for the following error:') + sTraceback)
        _logger.error(errorStyle('splitAudio: ' + errMsg))
        raise Exception(errMsg)
