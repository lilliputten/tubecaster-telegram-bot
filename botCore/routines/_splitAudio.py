# -*- coding:utf-8 -*-

import pathlib
import traceback
from typing import Callable


from core.logger import getDebugLogger, titleStyle, secondaryStyle
from core.appConfig import AUDIO_FILE_EXT
from core.helpers.errors import errorToString
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
    """
    try:
        _logger.info(f'splitAudio: Start creating pieces for file: {audioFileName}')

        probeData = probe(audioFileName)

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

        hasPieces = piecesCount > 1
        pieces = range(piecesCount)
        # realPiecesCount = len(pieces)
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
            # outputFileName = f'{outFilePrefix}{delimiter}{no}{AUDIO_FILE_EXT}'
            _logger.info(f'splitAudio: Creating piece {no}/{piecesCount} ({start}-{end}) -> {outputFileName})')
            split(audioFileName, outputFileName, start=start, end=end)
            if pieceCallback:
                pieceCallback(outputFileName, n, piecesCount)
            if removeFiles:
                pathlib.Path(outputFileName).unlink(missing_ok=True)

        _logger.info(f'splitAudio: Already created all {piecesCount} piece(s)')

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
