# -*- coding:utf-8 -*-

import time
import pathlib
import posixpath
import math
import os
import io
import sys
import traceback
import subprocess
import json
from typing import Callable

PROJECT_PATH = pathlib.Path(os.getcwd()).as_posix()
print('Project path:', PROJECT_PATH)
sys.path.insert(1, PROJECT_PATH)  # noqa  # pylint: disable=wrong-import-position

from core.helpers.errors import errorToString
from core.helpers.audio import getDesiredPiecesCount
from core.ffmpeg import probe, split

audioExt = '.mp4'

# Max audio file size for tg bot, in bytes
maxAudioFileSize = 20000

useGap = 1
removePieces = True

TCallback = Callable[[str, int, int], None]


def pieceCallback(filename: str, pieceNo: int, piecesCount: int):
    print('Callback:', filename, '-', pieceNo, '/', piecesCount)
    time.sleep(3)


def splitMp3(inFileName: str, outFilePrefix: str, piecesCount: int, pieceCallback: TCallback | None = None):
    try:
        print('Start: ' + inFileName)

        #  ffmpeg-python
        result = probe(inFileName)

        format = result.get('format', {})
        duration = float(format.get('duration', '0'))
        durationSec = math.ceil(duration)
        size = int(format.get('size', '0'))

        streams = result.get('streams', [{}])
        stream = streams[0]
        codecName = stream.get('codec_name')

        pieceDurationSec = duration / piecesCount

        #  print('Probe data:', json.dumps(result, indent=2, ensure_ascii=False))
        print('Audio codec:', codecName)
        print('Audio duration (secs):', duration)
        print('Audio duration (full secs):', durationSec)
        print('Audio size (bytes):', size)

        print('Pieces count:', piecesCount)
        print('Pieces duration (secs):', pieceDurationSec)

        for n in range(piecesCount):
            no = n + 1
            start = n * pieceDurationSec
            if useGap and n:
                start -= useGap
            end = (n + 1) * pieceDurationSec
            if useGap and n < piecesCount - 1:
                end += useGap
            outputFileName = f'{outFilePrefix}-{no}{audioExt}'
            print(f'Piece No {no} ({outputFileName}): {start}-{end}')
            split(inFileName, outputFileName, start=start, end=end)
            if pieceCallback:
                pieceCallback(outputFileName, n, piecesCount)
            if removePieces:
                pathlib.Path(outputFileName).unlink(missing_ok=True)

        print('Finished')

    except Exception as err:
        sError = errorToString(err)   # errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'splitMp3: Error processing sound: ' + sError
        print('splitMp3: Traceback for the following error:' + sTraceback)
        print(errMsg)


if __name__ == '__main__':
    # Project working folder
    cwd = pathlib.Path(os.getcwd()).as_posix()

    # Output folder
    outFolder = posixpath.join(cwd, 'tests/out')
    pathlib.Path(outFolder).mkdir(parents=True, exist_ok=True)
    print('Output folder:', outFolder)

    # Output file prefix
    outFilePrefix = posixpath.join(outFolder, 'test')

    # Test audio file (from args or default one)
    defaultAudio = 'tests/test-audios/test-short.mp3'
    #  defaultAudio = 'tests/test-audios/StarWars3.wav'
    #  defaultAudio = 'tests/test-audios/StarWars3.converted.mp3'
    filename = sys.argv[1] if len(sys.argv) > 1 else defaultAudio
    print('Input file name:', filename)
    inFileName = posixpath.join(cwd, filename)

    fileSize = os.path.getsize(inFileName)
    print('Input file size:', fileSize)
    print('Max file size:', maxAudioFileSize)

    piecesCount = getDesiredPiecesCount(fileSize, maxAudioFileSize)
    print('Pieces count:', piecesCount)

    # Go splitting
    splitMp3(inFileName, outFilePrefix, piecesCount, pieceCallback)
