from collections import namedtuple


_term = namedtuple('Term', 'term POS sense usage Pinyin')
_translation = namedtuple('Translation', 'original translations note')
_category = namedtuple('Category', 'translations')


class Result(object):
    def __init__(self, result):
        raise NotImplementedError


class Term(_term):
    def __str__(self):
        return '<Term[{self.term}] object at {1}>'.format(id(self), self=self)


class Translation(_translation):
    def __str__(self):
        return '<Translation object at {0}>'.format(id(self))


class Category(object):
    def __str__(self):
        return '<Category object at {0}>'.format(id(self))

    def __len__(self):
        return len(self._translations)