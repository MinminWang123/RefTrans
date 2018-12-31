import re
from Author import AuthorLF
import utils


class Reference(object):
    def __init__(self, original):
        self._original = original
        self._parsed = True
        self._year = ""
        self._authors = []

    def get_original(self):
        return self._original

    def is_parsed(self):
        return self._parsed

    def _parse_year(self):
        try:
            self._year = re.search('.*?\((.*?)\)\..*', self._original).group(1).strip()
            if len(self._year) == 0:
                self._parsed = False
                self._year = "error in year"
        except AttributeError:
            self._parsed = False
            self._year = "error in year"

    def get_year(self):
        self._parse_year()
        return self._year

    def _parse_authors(self):
        try:
            self._split_authors(re.search('(.*?)\(.*?\)\..*', self._original).group(1))
        except AttributeError:
            self._parsed = False
            self._authors = "error in author(s)"

    def get_authors(self):
        self._parse_authors()
        return self._authors

    def _split_authors(self, raw_text):
        authors = re.findall('\w.*?,(?:\s*[A-Z]\.)*', raw_text)
        for author in authors:
            self._authors.append(AuthorLF(author))
        if len(self._authors) == 0:
            self._parsed = False
            self._authors = "error in author(s)"

    def get_source(self):
        return utils.get_source(self._original)

    def _get_body(self):
        return utils.get_body(self._original)


def main():
    with open('Journal.txt', 'r') as file:
        for line in file.readlines():
            b = Reference(line)
            print("Original: " + line.strip())
            print("Source: " + b.get_source())
            print("Body: " + b._get_body())
            print()


if __name__ == "__main__":
    main()
