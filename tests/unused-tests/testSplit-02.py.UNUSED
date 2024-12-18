# -*- coding:utf-8 -*-

import pathlib
import posixpath
import math
import os
import sys
import traceback

import librosa
import soundfile as sf

from core.helpers.audio import getDesiredPiecesCount


maxDuration = 3
# Max audio file size for tg bot, in bytes
maxAudioFileSize = 20000


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


#  def getDesiredPiecesCount(fileSize: int, maxAudioFileSize: int):
#      if fileSize <= maxAudioFileSize:
#          return 1
#      return math.ceil(fileSize / maxAudioFileSize)


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
    print('[testSplit-02]: Max file size:', maxAudioFileSize)

    piecesCount = getDesiredPiecesCount(fileSize, maxAudioFileSize)
    print('[testSplit-02]: Pieces count:', piecesCount)

    # Go splitting
    splitMp3(inFileName, outFilePrefix, piecesCount)
