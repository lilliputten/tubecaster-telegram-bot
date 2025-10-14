# -*- coding:utf-8 -*-

import os
import traceback
from datetime import timedelta

import telebot  # pyTelegramBotAPI
from telebot import types

from botApp import botApp
from botCast.config.castConfig import demoVideo, logTraceback
from botCast.helpers.cleanFiles import cleanFiles
from botCast.helpers.downloadAudioFile import downloadAudioFile
from botCast.helpers.downloadInfo import downloadInfo
from botCore.helpers import replyOrSend
from botCore.types import YtdlOptionsType
from core.appConfig import TELEGRAM_OWNER_ID
from core.helpers.errors import errorToString
from core.helpers.files import sizeofFmt
from core.logger import getDebugLogger
from core.logger.utils import errorStyle, primaryStyle, secondaryStyle, titleStyle, warningStyle

_logger = getDebugLogger()

_doCleanFiles = False


def downloadAudioTest(url: str, chatId: str | int | None, username: str, message: types.Message | None = None):
    options: YtdlOptionsType | None = None

    try:
        rootMessage = replyOrSend('Fetching the video details...', chatId, message) if chatId else None
        options, videoInfo = downloadInfo(url, chatId, username)

        filesize = videoInfo.get('filesize')
        filesizeApprox = videoInfo.get('filesize_approx')
        sizeFmt = sizeofFmt(filesize if filesize else filesizeApprox)

        # DEBUG
        # cachedir = '.temp'
        # destFile = cachedir + '/file.mp3'
        # options['_destFolder'] = cachedir
        # options['cachedir'] = cachedir
        # options['_destFile'] = destFile
        # options['outtmpl'] = destFile
        # options['keepvideo'] = True

        details = ', '.join(
            list(
                filter(
                    None,
                    [
                        sizeFmt,
                        str(timedelta(seconds=int(videoInfo['duration']))) if videoInfo.get('duration') else None,
                        videoInfo.get('resolution'),  # '640x360'
                        str(videoInfo.get('fps')) + ' fps' if videoInfo.get('fps') else None,
                    ],
                )
            )
        )

        #  infoMsg = f'Going to start downloading the video "{title}" of size ({sizeFmt})...'
        infoMsg = ''.join(
            list(
                filter(
                    None,
                    [
                        'Extracting an audio from the video',
                        f' ({details})' if details else '',
                        '...',
                    ],
                )
            )
        )
        _logger.info(f'downloadAudioTest: Message: ' + infoMsg)
        #  replyOrSend(infoMsg, chatId, message)

        # Load audio from url...
        audioFile = downloadAudioFile(options, videoInfo)
        if not audioFile:
            raise Exception('Audio file name has not been defined')
        audioSize = os.path.getsize(audioFile)
        audioSizeFmt = sizeofFmt(audioSize)
        _logger.info(f'downloadAudioTest: Audio file {audioFile} (with size: {audioSizeFmt}) has been downloaded')
        infoMsg = ''.join(
            list(
                filter(
                    None,
                    [
                        'Ok, sending the audio',
                        f' ({audioSizeFmt})' if audioSizeFmt else '',
                        '...',
                    ],
                )
            )
        )
        _logger.info(f'downloadAudioTest: Message: ' + infoMsg)
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error fetching test audio file: ' + errText
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle('downloadAudioTest: Traceback for the following error:') + sTraceback)
        _logger.error(errorStyle('downloadAudioTest: ' + errMsg))
        # if chatId:
        #     replyOrSend(errMsg, chatId, message)
        #  raise Exception(errMsg)
    finally:
        # Remove temporary files and folders
        if options and _doCleanFiles:
            cleanFiles(options)


if __name__ == '__main__':
    try:
        downloadAudioTest(demoVideo, TELEGRAM_OWNER_ID, 'test', None)
    except Exception as err:
        print('ERROR:', repr(err))
