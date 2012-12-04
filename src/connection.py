# encoding=utf-8
import urllib
import urllib2
import StringIO
import gzip
import Cookie
import logging

logger = logging.getLogger('connection')


class Connection(object):
    def __init__(self, url):
        self.__url = url

    def setUrl(self, new_url):
        '''
        needed for redirect handling
        '''
        self.__url = new_url

    def sendRequest(self, data=None, cookies=None, getCookies=False):
        opener = urllib2.build_opener()
        opener.addheaders = self.getHeaders().items()
        if cookies is not None:
            opener.addheaders += [('Cookie', cookies)]
        if data is not None:
            data = urllib.urlencode(self.encode_dict(data))
        logger.info('request: ' + self.__url + ' ' + str(data))
        response = opener.open(self.__url, data)
        encoding = response.headers.getparam('charset')
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO.StringIO(response.read())
            gzip_f = gzip.GzipFile(fileobj=buf)
            content = gzip_f.read()
        else:
            content = response.read()
        content = content.decode(encoding)
        opener.close()
        logger.info('response: ' + content)
        if getCookies:
            return Cookie.SimpleCookie(response.info().get('Set-Cookie'))
        else:
            return content

    def encode_dict(self, params):
        return dict([(key, val.encode('utf-8')) for key, val in params.items()
                     if isinstance(val, basestring)])

    def getHeaders(self):
        return {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                              'rv:16.0) Gecko/20100101 Firefox/16.0',
                'Host': '95.163.80.22',
                'Connection': 'keep-alive',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'Accept': 'text/html,application/xhtml+xml,application/xml;'
                          'q=0.9,*/*;q=0.8'
                }
