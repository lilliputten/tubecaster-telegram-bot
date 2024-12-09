# -*- coding:utf-8 -*-

"""
A test for audio files splitting, using librosa

It uses soundfile, audioread and ffmpeg.

Ffmpeg library hould be installed manually in the system, see https://www.ffmpeg.org/download.html).

See stack overflow topic [Good choice might be librosa...](https://stackoverflow.com/a/77545091/28090454) for the source of the initial idea.
"""

import pathlib
import posixpath
import math
import os
import sys
import traceback

#  from core.helpers.errors import errorToString

import librosa
import soundfile as sf


maxDuration = 3
maxFileSize = 20000


def splitMp3(inFileName: str, outFilePrefix: str, piecesCount: int):
    try:
        print('[testSplit-02:splitMp3]: Start: ' + inFileName)
        data, sr = librosa.load(inFileName, sr=None)
        print('[testSplit-02:splitMp3]: Sound:', data, sr)

        totalChunks = len(data)
        #  pieceDurationSec = 3  # In seconds
        #  chunksPerPiece = math.ceil(pieceDurationSec * sr)
        chunksPerPiece = math.ceil(totalChunks / piecesCount)
        totalPieces = math.ceil(totalChunks / chunksPerPiece)

        piecePositions = [[p, p + chunksPerPiece] for p in range(0, totalChunks, chunksPerPiece)]
        print(f'[testSplit-02:splitMp3]: Piece positions ({totalPieces}):', piecePositions)

        for n, positions in enumerate(piecePositions):
            start, end = positions
            if end > totalChunks:
                end = totalChunks
            pieceData = data[start:end]
            no = n + 1
            outputFile = f'{outFilePrefix}-{no}.mp3'
            print(f'[testSplit-02:splitMp3]: Piece #{no} ({outputFile})')
            sf.write(outputFile, pieceData, sr)

    except Exception as err:
        sError = repr(err)   # errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'testSplit-02:splitMp3: Error processing sound: ' + sError
        print('testSplit-02:splitMp3: Traceback for the following error:' + sTraceback)
        print(errMsg)


def getDesiredPiecesCount(fileSize: int, maxFileSize: int):
    if fileSize <= maxFileSize:
        return 1
    return math.ceil(fileSize / maxFileSize)


if __name__ == '__main__':
    # Project working folder
    cwd = pathlib.Path(os.getcwd()).as_posix()

    # Output folder
    outFolder = posixpath.join(cwd, 'tests/out')
    pathlib.Path(outFolder).mkdir(parents=True, exist_ok=True)
    print('[testSplit-02]: Output folder:', outFolder)

    # Output file prefix
    outFilePrefix = posixpath.join(outFolder, 'test')

    # Test audio file (from args or default one)
    defaultAudio = 'tests/test-audios/test-short.mp3'
    filename = sys.argv[1] if len(sys.argv) > 1 else defaultAudio
    print('[testSplit-02]: Input file name:', filename)
    inFileName = posixpath.join(cwd, filename)

    fileSize = os.path.getsize(inFileName)
    print('[testSplit-02]: Input file size:', fileSize)
    print('[testSplit-02]: Max file size:', maxFileSize)

    piecesCount = getDesiredPiecesCount(fileSize, maxFileSize)
    print('[testSplit-02]: Pieces count:', piecesCount)

    # Go splitting
    splitMp3(inFileName, outFilePrefix, piecesCount)
