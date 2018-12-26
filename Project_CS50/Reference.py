import re
from Author import AuthorLF


class Reference(object):
    def __init__(self, original):
        self._original = original
        self._parsed = True
        self._year = ""
        self._authors = []

    def getOriginal(self):
        return self._original

    def isParsed(self):
        return self._parsed

    def _parseYear(self):
        try:
            self._year = re.search('.*?\((.*?)\)\..*', self._original).group(1).strip()
            if len(self._year) == 0:
                self._parsed = False
                self._year = "error in year"
        except AttributeError:
            self._parsed = False
            self._year = "error in year"

    def getYear(self):
        self._parseYear()
        return self._year

    def _parseAuthors(self):
        try:
            self._splitAuthors(re.search('(.*?)\(.*?\)\..*', self._original).group(1))
        except AttributeError:
            self._parsed = False
            self._authors = "error in author(s)"

    def getAuthors(self):
        self._parseAuthors()
        return self._authors

    def _splitAuthors(self, rawText):
        authors = re.findall('\w.*?,(?:\s*[A-Z]\.)*', rawText)
        for author in authors:
            self._authors.append(AuthorLF(author))
        if len(self._authors) == 0:
            self._parsed = False
            self._authors = "error in author(s)"
