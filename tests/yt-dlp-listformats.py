# -*- coding:utf-8 -*-

import pathlib
import posixpath
import re
import os
import traceback

import yt_dlp


YTDL = yt_dlp


# url = 'https://www.youtube.com/watch?v=EngW7tLk6R8' # Small test fragment
url = 'https://www.youtube.com/watch?v=VgyQ-1tzFaY'   # Autodubbed


def run():
    try:
        ydl_opts = {'listformats': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            for f in info['formats']:   # type: ignore
                print(
                    f"{f['format_id']}: {f.get('acodec')} {f.get('abr')}k {f.get('language', 'unknown')} {f.get('tbr')}k"
                )
    except Exception as err:
        errText = repr(err)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error: ' + errText
        print('Traceback for the following error:' + sTraceback)
        print(errMsg)
        # raise Exception(errMsg)


# formats item raw data:
# {'format_id': '234-1', 'format_note': 'Русский - original (default)', 'format_index': None, 'url': 'https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1754444558/ei/rl6SaN6DGLDQpt8Pwerf6Q0/ip/103.252.119.249/id/560c90fb5b7315a6/itag/234/source/youtube/requiressl/yes/ratebypass/yes/pfa/1/goi/133/sgoap/clen%3D45866201%3Bdur%3D2834.018%3Bgir%3Dyes%3Bitag%3D140%3Blmt%3D1754173709538997%3Bxtags%3Dacont%3Doriginal:lang%3Dru/rqh/1/hls_chunk_host/rr3---sn-i3belnl6.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/met/1754422958,/mh/vJ/mm/31,29/mn/sn-i3belnl6,sn-i3b7knld/ms/au,rdu/mv/m/mvi/3/pl/24/rms/au,au/initcwndbps/685000/bui/AY1jyLOmrqWcMeMKQ8LM2UIUmAKG0TsJDOCB7CkaVgLxuXHzSwE5BVIypt4z7MqlT6BEQp7xUcfDVCZg/spc/l3OVKWqO6EQOnypmhfF3/vprv/1/playlist_type/DVR/dover/13/txp/4532534/mt/1754422443/fvip/2/short_key/1/keepalive/yes/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,pfa,goi,sgoap,rqh,xpc,bui,spc,vprv,playlist_type/sig/AJfQdSswRQIhAN1WWAclA4fPuFNDXD8Jbe97H_WmMqE_K08UT7dvncMgAiBvPAppBoCO8xyQcE-338BJXJiNj9wcw9Z1ue0xmi5K-g%3D%3D/lsparams/hls_chunk_host,met,mh,mm,mn,ms,mv,mvi,pl,rms,initcwndbps/lsig/APaTxxMwRgIhAOqQMdRZ-FzTE6P2bM9JPeJv5RxMrpf-FsNHXHNHnBpHAiEAhSqpTsJ9B0uMWCUdo29ujSlTAs3vD5owhJ6SSddGa78%3D/playlist/index.m3u8', 'manifest_url': 'https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1754444558/ei/rl6SaN6DGLDQpt8Pwerf6Q0/ip/103.252.119.249/id/560c90fb5b7315a6/source/youtube/requiressl/yes/xpc/EgVo2aDSNQ%3D%3D/playback_host/rr3---sn-i3belnl6.googlevideo.com/met/1754422958%2C/mh/vJ/mm/31%2C29/mn/sn-i3belnl6%2Csn-i3b7knld/ms/au%2Crdu/mv/m/mvi/3/pl/24/rms/au%2Cau/tx/51548074/txs/51548072%2C51548073%2C51548074%2C51548075%2C51548076%2C51548077/hfr/1/demuxed/1/tts_caps/1/maudio/1/initcwndbps/685000/bui/AY1jyLOmrqWcMeMKQ8LM2UIUmAKG0TsJDOCB7CkaVgLxuXHzSwE5BVIypt4z7MqlT6BEQp7xUcfDVCZg/spc/l3OVKWqO6EQOnypmhfF3/vprv/1/go/1/rqh/5/mt/1754422443/fvip/2/nvgoi/1/short_key/1/ncsapi/1/keepalive/yes/dover/13/itag/0/playlist_type/DVR/sparams/expire%2Cei%2Cip%2Cid%2Csource%2Crequiressl%2Cxpc%2Ctx%2Ctxs%2Chfr%2Cdemuxed%2Ctts_caps%2Cmaudio%2Cbui%2Cspc%2Cvprv%2Cgo%2Crqh%2Citag%2Cplaylist_type/sig/AJfQdSswRQIgUNVA59WNy2AiD_cE4JEOpiTQi9qDDOwsYGyjRKoaF8ECIQD-I1_nZ5ThAAfmfTC0MQgenKWQzgYouqYT2wRpJGGz4w%3D%3D/lsparams/playback_host%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps/lsig/APaTxxMwRQIgYT4jqMXPiexyIak5yDPQ_z4zeDKkBETjOd7zhFJfRmkCIQCH7ppaK5JCcNWVv77x5d3kOPR0qleZbB66FmXhzXopNQ%3D%3D/file/index.m3u8', 'language': 'ru', 'ext': 'mp4', 'protocol': 'm3u8_native', 'preference': None, 'quality': -1, 'has_drm': False, 'vcodec': 'none', 'source_preference': -1, 'language_preference': 10, 'audio_ext': 'mp4', 'video_ext': 'none', 'vbr': 0, 'abr': None, 'tbr': None, 'resolution': 'audio only', 'aspect_ratio': None, 'http_headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-us,en;q=0.5', 'Sec-Fetch-Mode': 'navigate'}, 'format': '234-1 - audio only (Русский - original (default))'}

if __name__ == '__main__':
    run()
