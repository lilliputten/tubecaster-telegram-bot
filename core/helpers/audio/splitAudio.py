# -*- coding:utf-8 -*-

import pathlib
import traceback
from typing import Callable

from core.logger import getLogger
from core.appConfig import AUDIO_FILE_EXT
from core.helpers.errors import errorToString
from core.ffmpeg import probe, split

TPieceCallback = Callable[[str, int, int], None]

logTraceback = False

_logger = getLogger('bot/botRoutes')


def splitAudio(
    inFileName: str,
    outFilePrefix: str,
    piecesCount: int,
    pieceCallback: TPieceCallback | None = None,
    gap: int = 0,
    removeFiles: bool = True,
):
    """
    Split large audio file into pieces via ffmpeg (should be installed in the system).

    Parameters:

    - inFileName: Input audio path.
    - outFilePrefix: Output file prefix. Will be extended by `-{no}{.ext}`.
    - piecesCount: Desired pieces count.
    - pieceCallback: Callback to process each piece, when file has already been
      written. Next parameteres will be passed: filename, piece count, tital pieces number.
    - gap: Add an overlapping gap (in seconds) at the place of pieces junction. 0 to no gaps.
    - removeFiles: Automatically remove piece files when done (after callback return, if specified).
    """
    try:
        _logger.info(f'splitAudio: Start creating pieces for file: {inFileName}')

        probeData = probe(inFileName)

        format = probeData.get('format', {})
        duration = float(format.get('duration', '0'))
        pieceDurationSec = duration / piecesCount

        #  # DEBUG: Show debug info (keep this while developing)
        #  durationSec = math.ceil(duration)
        #  size = int(format.get('size', '0'))
        #  streams = probeData.get('streams', [{}])
        #  stream = streams[0]
        #  codecName = stream.get('codec_name')
        #  #  print('Probe data:', json.dumps(probeData, indent=2, ensure_ascii=False))
        #  # print('Audio codec:', codecName)
        #  print('Audio duration (secs):', duration)
        #  # print('Audio duration (full secs):', durationSec)
        #  # print('Audio size (bytes):', size)
        #  print('Pieces count:', piecesCount)
        #  print('Pieces duration (secs):', pieceDurationSec)

        for n in range(piecesCount):
            no = n + 1
            start = n * pieceDurationSec
            if gap and n:
                start -= gap
            end = (n + 1) * pieceDurationSec
            if gap and n < piecesCount - 1:
                end += gap
            outputFileName = f'{outFilePrefix}-{no}{AUDIO_FILE_EXT}'
            _logger.info(f'splitAudio: Creating piece {no}/{piecesCount} ({start}-{end}) -> {outputFileName})')
            split(inFileName, outputFileName, start=start, end=end)
            if pieceCallback:
                pieceCallback(outputFileName, n, piecesCount)
            if removeFiles:
                pathlib.Path(outputFileName).unlink(missing_ok=True)

        _logger.info(f'splitAudio: Already created all {piecesCount} pieces')

    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Audio splitting error: ' + errText
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('splitAudio: Traceback for the following error:' + sTraceback)
        _logger.error('splitAudio: ' + errMsg)
        raise Exception(errMsg)
