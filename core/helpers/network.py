# -*- coding:utf-8 -*-

from flask import request


def getRemoteAddr():
    """
    NOTE: It's not possible to get the remote address on the VDS server under VLESS proxy (TODO?)
    """
    # request.remote_addr
    if 'X-Forwarded-For' in request.headers:
        proxy_data = request.headers['X-Forwarded-For']
        ip_list = proxy_data.split(',')
        return ip_list[0]  # first address in list is User IP
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']
