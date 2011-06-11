# -*- coding: utf-8 -*-

'''
© WordReference.com
© 2011 Michele Lacchia
'''


import sys
import json
import urllib2
try:
    from PyQt4 import QtGui, QtCore, QtWebKit
except ImportError:
    try:
        from PySide import QtGui, QtCore, QtWebKit
    except ImportError:
        sys.exit('You must have PyQt4 or PySide installed to work with wordref. This is due to WordReference API, which requires Javascript evaluation.')

from objects import Result, Category, Translation, Term

## Function to render an HTML page with Javascript
def render(url):
    class _Render(QtWebKit.QWebPage):
        def __init__(self, url):
            self.app = QtGui.QApplication(sys.argv)
            QtWebKit.QWebPage.__init__(self)
            self.loadFinished.connect(self._loadFinished)
            self.mainFrame().load(QtCore.QUrl(url))
            self.app.exec_()
        def _loadFinished(self, result):
            self.frame = self.mainFrame()
            self.app.quit()

    r = _Render(url)
    return unicode(r.frame.toHtml())


DICTIONARIES = [
    'ar',
    'zh',
    'cz',
    'en',
    'fr',
    'gr',
    'it',
    'ja',
    'ko',
    'pl',
    'pt',
    'ro',
    'es',
    'tr'
]



class WordRefError(Exception):
    '''Base class for all wordref's errors.'''

class ApiError(WordRefError):
    '''Raised when user request cannot be accomplished by the API.'''

class ParsingError(WordRefError):
    '''Raised when errors occur during the parsing.'''


class Api(object):
    def __init__(self, user_id, code, api_version=None):
        self.user_id = user_id
        if len(code) == 2:
            raise ApiError('Monolingual dictionaries are not available yet')
        elif len(code) != 4:
            raise ApiError('Wrong dictionary code')
        elif code == 'esen':
            raise ApiError('Spanish - English dictionary does not support Json API')
        
        self.code = code
        self.api_version = api_version

    def __repr__(self):
        return 'Api(user_id={0}, code={1}, api_version={2})'.format(self.user_id,
                                                                    self.code,
                                                                    self.api_version or 'last')

    def __str__(self):
        return '<Api[{0}] at {1}>'.format(self.code, id(self))

    def search(self, term):
        url = self._build_url(term)
        data = render(urllib2.urlopen(url).read())
        print url, data
        try:
            start = data.index('<{')
            end = data.index('</pre')
        except ValueError:
            raise WordRefError('Cannot parse JSON: malformed response')
        try:
            return self._parse_result(data[start:end])
        except Exception as e:
            try:
                msg = e.args[0]
            except IndexError:
                msg = repr(e)
            raise ParsingError(msg)

    def _build_url(self, term):
        if self.api_version is None:
            base = 'http://api.wordreference.com/{self.user_id}/json/{self.code}/{0}'
        else:
            base = 'http://api.wordreference.com/{self.api_version}/{self.user_id}/json/{self.code}/{0}'
        return base.format(term, self=self)

    def _parse_result(self, data):
        data = json.loads(data)
        result = []
        for term, categories in data.iteritems():
            if term in ('Lines', 'END'):
                continue
            for category, translations in data[term].iteritems():
                tr = []
                for _, trans in translations.iteritems():
                    tr.append(Translation(trans))
                result.append(Category(category, tr))
        return Result(result)
