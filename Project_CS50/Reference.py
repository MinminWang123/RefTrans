"""
file: Reference.py
define Reference
"""


import re
from Author import AuthorLF
import utils
from Handler import *
import CodeBook

"""
class Reference
initialize:   Reference(str original)
get_original: return str original
is_parsed:    return True if successfully parsed, False if any field fails
get_authors:  return a list of Author / str "error in author(s)"
get_year:     return str year / "error in year"
get_source:   return str source if present, "" otherwise

encode_authors(): return Handler.authors
encode_year():    return Handler.general
encode_source():  return Handler.general
"""


class Reference(object):
    def __init__(self, original):
        self._original = original
        self._parsed = True

    def get_original(self):
        return self._original

    def is_parsed(self):
        return self._parsed

    def _parse_authors(self):
        self._authors = []
        try:
            self._split_authors(re.search(r'(.*?)\(.*?\)\..*', self._original).group(1))
        except AttributeError:
            self._parsed = False
            self._authors = "error in author(s)"

    def get_authors(self):
        self._parse_authors()
        return self._authors

    def _split_authors(self, raw_text):
        authors = re.findall(r'\w.*?,(?:\s*-?[A-Z]\.)*', raw_text)
        for author in authors:
            self._authors.append(AuthorLF(author))
        if len(self._authors) == 0:
            self._parsed = False
            self._authors = raw_text.strip()

    def encode_authors(self, dic):
        return Handler.authors(self.get_authors(), dic)

    def _parse_year(self):
        self._year = ""
        try:
            self._year = re.search(r'.*?\((.*?)\)\..*', self._original).group(1).strip()
            if len(self._year) == 0:
                self._parsed = False
                self._year = "error in year"
        except AttributeError:
            self._parsed = False
            self._year = "error in year"

    def get_year(self):
        self._parse_year()
        return self._year

    def encode_year(self, dic):
        return Handler.general(self.get_year(), dic)

    def get_source(self):
        return utils.get_source(self._original)

    def encode_source(self, dic):
        return Handler.general(self.get_source(), dic)

    def _get_body(self):
        return utils.get_body(self._original)


def main():
    # with open('test_cases/JournalPublished.txt', 'r') as file:
    #     for line in file.readlines():
    #         b = Reference(line)
    #         print("Original: " + line.strip())
    #         print("Source: " + b.get_source())
    #         print("Body: " + b._get_body())
    #         print("Authors: " + b.encode_authors(char_end="", char_int="", ln_end=""))
    #         print()

    text = "Aiken, L. S., & West, S. G. (1991). Multiple regression: Testing and interpreting interactions. Newbury Park, CA: Sage."
    ref = Reference(text)
    print(ref.encode_authors(CodeBook.AMJ["authors"]))
    print(ref.encode_year(CodeBook.AMJ['year']))


if __name__ == "__main__":
    main()
