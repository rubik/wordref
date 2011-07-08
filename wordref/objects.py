'''
Example:

http://api.wordreference.com/{user_id}/json/enit/python

+ Result
|
+ term0 +
        |
        + Category(PrincipalTranslations) +
        |                                 |
        |                                 + Translation +
        |                                 |             |
        |                                 |             + Term
        |                                 |             + Term
        |                                 |             + Note
        |                                 |
        |                                 + Translation +
        |                                               |
        |                                               + Term
        |                                               + Term
        |                                               + Note
        + Category(Compounds) +
                              |
                              + Translation +
                                            |
                                            + Term
                                            + Term
                                            + Note
'''


from collections import namedtuple


__all__ = ['Result', 'Category', 'Translation', 'Term']

_result = namedtuple('Result', 'categories')


class Result(object):

    def __init__(self, r={}):
        self._r = r

    def add(self, name, category):
        self._r[name] = category

    @ property
    def principal(self):
        return self._r['PrincipalTranslations']

    @ property
    def additional(self):
        return self._r['AdditionalTranslations']

    @ property
    def compounds(self):
        return self._r['Compounds']

    def __repr__(self):
        n = len(self._r)
        suffix = ['ies', 'y'][n == 1]
        return '<Result [{0} categor{1}]>'.format(n, suffix)


class Translation(object):

    def __init__(self, t):
        self.original = Term(**t['OriginalTerm'])
        self.first_t = Term(**t['FirstTranslation'])
        self._translations = []
        for key, term in t.iteritems():
            if key in ('OriginalTerm', 'FirstTranslation', 'Note'):
                continue
            self._translations.append(Term(**term))
        self.note = t['Note'] or None

    @ property
    def first(self):
        return self.first_t

    @ property
    def translations(self):
        return [self.first] + self._translations

    def __repr__(self):
        return '<Translation[{0}>{1}] object at {2}>'.format(self.original.term,
                                                             ','.join(map(str, self.translations)),
                                                             hex(id(self)))


class Term(object):

    _fields = ('term', 'POS', 'sense', 'usage', 'Pinyin')

    def __init__(self, **kwargs):
        self.term, self.pos, self.sense, self.usage, self.pinyin = map(self._get_values(kwargs), Term._fields)

    def __repr__(self):
        return '<Term[{0}] object at {1}>'.format(self.term, hex(id(self)))

    def __str__(self):
        return unicode(self.term)

    def _get_values(self, kwargs):
        def _get(item):
            value = kwargs.get(item, None)
            if not value:
                return None
            return value
        return _get