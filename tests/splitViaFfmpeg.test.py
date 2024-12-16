# -*- coding:utf-8 -*-

import time
import pathlib
import posixpath
import os
import sys

# Inject project path to allow server-side tests
PROJECT_PATH = pathlib.Path(os.getcwd()).as_posix()
print('Project path:', PROJECT_PATH)
sys.path.insert(1, PROJECT_PATH)

from core.helpers.audio import getDesiredPiecesCount, splitAudio

# Max audio file size for tg bot, in bytes
maxAudioFileSize = 20000


def pieceCallback(filename: str, pieceNo: int, piecesCount: int):
    print('Callback:', filename, '-', pieceNo, '/', piecesCount)
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
    inFileName = posixpath.join(cwd, filename)

    fileSize = os.path.getsize(inFileName)
    print('Input file size:', fileSize)
    print('Max file size:', maxAudioFileSize)

    piecesCount = getDesiredPiecesCount(fileSize, maxAudioFileSize)
    print('Pieces count:', piecesCount)

    # Go splitting
    splitAudio(inFileName, outFilePrefix, piecesCount, pieceCallback)
