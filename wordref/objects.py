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


_term = namedtuple('Term', 'term POS sense usage Pinyin')
_translation = namedtuple('Translation', 'original translations note')
_category = namedtuple('Category', 'name translations')
_result = nameduple('Result', 'categories')


class Result(_result):
    def __str__(self):
        return '<Result object at {0}>'.format(id(self))


class Category(object):
    def __str__(self):
        return '<Category object at {0}>'.format(id(self))

    def __len__(self):
        return len(self._translations)


class Translation(_translation):
    def __str__(self):
        return '<Translation object at {0}>'.format(id(self))


class Term(_term):
    def __str__(self):
        return '<Term[{self.term}] object at {1}>'.format(id(self), self=self)