# -*- coding:utf-8 -*-

import time
import pathlib
import posixpath
import os
import sys

from botCore.helpers import getDesiredPiecesCount
from botCore.routines import splitAudio

# Inject project path to allow server-side tests
PROJECT_PATH = pathlib.Path(os.getcwd()).as_posix()
print('Project path:', PROJECT_PATH)
sys.path.insert(1, PROJECT_PATH)

# from core.helpers.audio import getDesiredPiecesCount, splitAudio

# Max audio file size for tg bot, in bytes
maxAudioFileSize = 20000


def pieceCallback(audioFileName: str, pieceNo: int | None, piecesCount: int | None):
    print('Callback:', audioFileName, '-', str(pieceNo), '/', str(piecesCount))
    time.sleep(3)


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
    audioFileName = posixpath.join(cwd, filename)

    fileSize = os.path.getsize(audioFileName)
    print('Input file size:', fileSize)
    print('Max file size:', maxAudioFileSize)

    piecesCount = getDesiredPiecesCount(fileSize, maxAudioFileSize)
    print('Pieces count:', piecesCount)

    # Go splitting
    splitAudio(audioFileName, outFilePrefix, piecesCount, pieceCallback)
