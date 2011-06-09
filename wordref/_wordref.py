# -*- coding: utf-8 -*-

'''
© WordReference.com
© 2011 Michele Lacchia
'''


import json
import urllib2

from objects import Result, Category, Translation, Term


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

TEST_DATA = '''{"term0":{"PrincipalTranslations":{"0":{"OriginalTerm":{"term":"key","POS":"n","sense":"for a lock","usage":""},"FirstTranslation":{"term":"chiave","POS":"nf","sense":""},"Note":""},"1":{"OriginalTerm":{"term":"key","POS":"n","sense":"for a code","usage":""},"FirstTranslation":{"term":"parola chiave","POS":"nf","sense":""},"SecondTranslation":{"term":"password","POS":"nf","sense":""},"Note":""},"2":{"OriginalTerm":{"term":"key","POS":"n","sense":"on a typewriter, keyboard","usage":""},"FirstTranslation":{"term":"tasto","POS":"nm","sense":""},"Note":""},"3":{"OriginalTerm":{"term":"key","POS":"n","sense":"music: D major, etc.","usage":""},"FirstTranslation":{"term":"chiave","POS":"nf","sense":"musica"},"Note":""},"4":{"OriginalTerm":{"term":"key","POS":"n","sense":"tone of a voice","usage":""},"FirstTranslation":{"term":"tono","POS":"nm","sense":""},"Note":""},"5":{"OriginalTerm":{"term":"key","POS":"adj","sense":"most important","usage":""},"FirstTranslation":{"term":"chiave","POS":"nf","sense":""},"Note":""}},"AdditionalTranslations":{"0":{"OriginalTerm":{"term":"key","POS":"n","sense":"for a map","usage":""},"FirstTranslation":{"term":"scala","POS":"nf","sense":""},"Note":""},"1":{"OriginalTerm":{"term":"key","POS":"n","sense":"dictionary","usage":""},"FirstTranslation":{"term":"legenda, chiave","POS":"nf","sense":""},"Note":""},"2":{"OriginalTerm":{"term":"key","POS":"n","sense":"for a problem, solution","usage":""},"FirstTranslation":{"term":"chiave","POS":"nf","sense":""},"Note":""},"3":{"OriginalTerm":{"term":"key","POS":"n","sense":"on a piano, etc.","usage":""},"FirstTranslation":{"term":"tasto","POS":"nm","sense":""},"Note":""},"4":{"OriginalTerm":{"term":"key","POS":"n","sense":"on a mechanism, for winding","usage":""},"FirstTranslation":{"term":"chiavetta","POS":"nf","sense":""},"Note":""},"5":{"OriginalTerm":{"term":"key","POS":"n","sense":"means of access","usage":""},"FirstTranslation":{"term":"chiave giusta","POS":"nf","sense":""},"SecondTranslation":{"term":"fattore chiave","POS":"nm","sense":""},"Note":""},"6":{"OriginalTerm":{"term":"key","POS":"n","sense":"style, tone","usage":""},"FirstTranslation":{"term":"stile","POS":"nm","sense":""},"SecondTranslation":{"term":"tono","POS":"nm","sense":""},"Note":""},"7":{"OriginalTerm":{"term":"key","POS":"n","sense":"keystone","usage":""},"FirstTranslation":{"term":"chiave di volta","POS":"nf","sense":""},"Note":""},"8":{"OriginalTerm":{"term":"key","POS":"n","sense":"island reef","usage":""},"FirstTranslation":{"term":"scogliera","POS":"nf","sense":""},"Note":""},"9":{"OriginalTerm":{"term":"key","POS":"vtr","sense":"type","usage":""},"FirstTranslation":{"term":"digitare","POS":"vtr","sense":""},"Note":""},"10":{"OriginalTerm":{"term":"key","POS":"vtr","sense":"lock","usage":""},"FirstTranslation":{"term":"inchiavare","POS":"vtr","sense":"raro, antiquato"},"SecondTranslation":{"term":"chiudere a chiave","POS":"vtr","sense":""},"Note":""},"11":{"OriginalTerm":{"term":"key","POS":"vtr","sense":"set pitch of musical instrument","usage":""},"FirstTranslation":{"term":"accordare","POS":"vtr","sense":""},"Note":""},"12":{"OriginalTerm":{"term":"key","POS":"vtr","sense":"cross-reference","usage":""},"FirstTranslation":{"term":"inserire","POS":"vtr","sense":""},"Note":""}}},"original":{"Compounds":{"0":{"OriginalTerm":{"term":"cross keys","POS":"","sense":"","usage":""},"FirstTranslation":{"term":"chiavi","POS":"","sense":""},"Note":""},"1":{"OriginalTerm":{"term":"piano keys","POS":"","sense":"","usage":""},"FirstTranslation":{"term":"tasti del pianoforte","POS":"","sense":""},"Note":""}}},"Lines":"End Reached","END":true}'''

class WordRefError(Exception):
    '''Base class for all wordref's errors.'''

class ApiError(WordRefError):
    '''Raised when an error is thrown by the API.'''

class ParsingError(WordRefError):
    '''Raised when errors occur during the parsing.'''


class Api(object):
    def __init__(self, user_id, code, api_version=None):
        self.user_id = user_id
        if len(code) == 2:
            raise ApiError('Monolingual dictionaries are not available yet')
        if code == 'esen':
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
        data = urllib2.urlopen(url).read()
        return self._parse_result(TEST_DATA)

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
