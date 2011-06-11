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
_category = namedtuple('Category', 'name translations')


class Result(_result):
    @ property
    def principal(self):
        return self._choose('PrincipalTranslations')

    @ property
    def additional(self):
        return self._choose('AdditionalTranslations')

    @ property
    def compounds(self):
        return self._choose('Compounds')

    def __repr__(self):
        return '<Result object at {0}>'.format(hex(id(self)))

    def _choose(self, name):
        for c in self.categories:
            if c.name == name:
                return c


class Category(_category):
    def __repr__(self):
        return '<Category[{0}] object at {1}>'.format(self.name, hex(id(self)))

    def __len__(self):
        return len(self._translations)


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