# -*- coding:utf-8 -*-

# NOTE: 2024.12.09, 00:48 -- It doesn't work: wrong format RuntimeError: ('Unsupported format:', '0xf', 'header:', '0xffff54d0')

import pathlib
import posixpath
import re
import os

import struct
import sys

# MP3 frames are not independent because of the byte reservoir. This script does not account for
# that in determining where to do the split.


def SplitMp3(fi, splitSec, out):

    # Constants for MP3
    bitrates = {
        0x0: 'free',
        0x1: 32,
        0x2: 40,
        0x3: 48,
        0x4: 56,
        0x5: 64,
        0x6: 80,
        0x7: 96,
        0x8: 112,
        0x9: 128,
        0xA: 160,
        0xB: 192,
        0xC: 224,
        0xD: 256,
        0xE: 320,
        0xF: 'bad',
    }
    freqrates = {0x0: 44100, 0x1: 48000, 0x2: 32000, 0x3: 'reserved'}
    countMpegFrames = 0
    frameDuration = 0.026
    unrecognizedBytes = 0
    splitFrame = int(round(splitSec / frameDuration))

    while True:

        startPos = fi.tell()

        # Check for 3 byte headers
        id3Start = fi.read(3)
        if len(id3Start) == 3:

            if id3Start == b'TAG':
                print('Found ID3 v1/1.1 header')
                fi.seek(startPos + 256)
                continue

            if id3Start == b'ID3':
                # Possibly a ID3v2 header
                majorVer, minorVer, flags, encSize = struct.unpack('>BBBI', fi.read(7))
                if majorVer != 0xFF and minorVer != 0xFF:
                    encSize1 = (encSize & 0x7F000000) >> 24
                    encSize2 = (encSize & 0x7F0000) >> 16
                    encSize3 = (encSize & 0x7F00) >> 8
                    encSize4 = encSize & 0x7F
                    if encSize1 < 0x80 and encSize2 < 0x80 and encSize3 < 0x80 and encSize4 < 0x80:
                        size = (
                            ((encSize & 0x7F000000) >> 3)
                            + ((encSize & 0x7F0000) >> 2)
                            + ((encSize & 0x7F00) >> 1)
                            + (encSize & 0x7F)
                        )
                        unsync = (flags >> 7) & 0x1
                        extendedHeader = (flags >> 6) & 0x1
                        experimental = (flags >> 5) & 0x1
                        print('Found ID3v2 header')
                        print('version', majorVer, minorVer, unsync, extendedHeader, experimental)
                        print('size', size)
                        # TODO extendedHeader not supported yet

                        fi.seek(startPos + 10 + size)
                        continue

        # Check for 4 byte headers
        fi.seek(startPos)
        headerRaw = fi.read(4)
        if len(headerRaw) == 4:
            headerWord = struct.unpack('>I', headerRaw)[0]

            # Check for MPEG-1 audio frame
            if headerWord & 0xFFF00000 == 0xFFF00000:
                print('Possible MPEG-1 audio header', hex(headerWord))
                countMpegFrames += 1
                ver = (headerWord & 0xF0000) >> 16
                bitrateEnc = (headerWord & 0xF000) >> 12
                freqEnc = (headerWord & 0xF00) >> 8
                mode = (headerWord & 0xF0) >> 4
                cpy = headerWord & 0xF
                if ver & 0xE == 0xA and freqEnc != 0xF:
                    print('Probably an MP3 frame')
                    bitrate = bitrates[bitrateEnc]
                    freq = freqrates[freqEnc >> 2]
                    padding = ((freqEnc >> 1) & 0x1) == 1
                    print('bitrate', bitrate, 'kbps')
                    print('freq', freq, 'Hz')
                    print('padding', padding)
                    frameLen = int((144 * bitrate * 1000 / freq) + padding)

                    # Copy frame to output
                    fi.seek(startPos)
                    frameData = fi.read(frameLen)
                    if countMpegFrames >= splitFrame:
                        out.write(frameData)

                    fi.seek(startPos + frameLen)
                    continue
                else:
                    raise RuntimeError('Unsupported format:', hex(ver), 'header:', hex(headerWord))

        # If no header can be detected, move on to the next byte
        fi.seek(startPos)
        nextByteRaw = fi.read(1)
        if len(nextByteRaw) == 0:
            break   # End of file
        unrecognizedBytes += 1

    print('unrecognizedBytes', unrecognizedBytes)
    print('countMpegFrames', countMpegFrames)
    print('duration', countMpegFrames * frameDuration, 'sec')


if __name__ == '__main__':
    fi = open(sys.argv[1], 'rb')
    out = open('test.mp3', 'wb')
    SplitMp3(fi, 30.0, out)
    out.close()
