from core.helpers.files import sizeofFmt

from ..types._TVideoInfo import TVideoInfo


def getFormattedVideoFileSize(videoInfo: TVideoInfo):
    filesize = videoInfo.get('filesize')
    filesizeApprox = videoInfo.get('filesize_approx')
    return sizeofFmt(filesize if filesize else filesizeApprox)
