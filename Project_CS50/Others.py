from Reference import Reference
import utils
import re
import Defs
import Parser

"""
OnLineJournal: author, year, title, journal, (Retrieved from) Source
API:
get_category()
get_title()
get_journal()
get_source()
"""


class OnLineJournal(Reference):

    def __init__(self, original):
        Reference.__init__(self, original)
        self._category = Defs.OnLineJournal

    def get_category(self):
        return self._category

    def _parse_title(self):
        self._parse_journal()
        if self.get_journal() == "error in journal":
            exp = "^(.*)[\.\?\!]\s"
        else:
            exp = "(.*)" + self.get_journal()
        try:
            self._title = re.search(exp, self._get_body()).group(1).strip()
            if len(self._title) == 0:
                self._parsed = False
                self._title = "error in title"
        except AttributeError:
            self._parsed = False
            self._title = "error in title"

    def get_title(self):
        self._parse_title()
        return self._title.strip(".")

    def _parse_journal(self):
        exp = re.sub("\?", '.', self._get_body())
        exp = re.sub("!", '.', exp)
        try:
            self._journal = re.search(".*\.(.+?)\.", exp).group(1).strip()
            if len(self._journal) == 0:
                self._parsed = False
                self._journal = "error in journal"
        except AttributeError:
            self._parsed = False
            self._journal = "error in journal"

    def get_journal(self):
        self._parse_journal()
        return self._journal


class Website(Reference):
    # author, year, title, (Retrieved from) Source
    def __init__(self, original):
        Reference.__init__(self, original)
        self._category = Defs.Website

    def get_category(self):
        return self._category

    def _parse_author(self):
        try:
            self._authors = re.search("(.+?)\.*\s*\(", self._original).group(1).strip()
        except AttributeError:
            self._parsed = False
            self._authors = "error in author"

    def get_authors(self):
        if re.search("\w.*?,(?:\s*[A-Z]\.)*", re.search("(.*?)\(", self._original).group(1)):
            return Reference.get_authors(self)
        else:
            self._parse_author()
            return [self._authors, ]

    def get_title(self):
        try:
            return re.search("^(.+)\.", self._get_body()).group(1).strip()
        except AttributeError:
            self._parsed = False
            return "error in title"

    def get_source(self):
        return utils.get_source(self._original)


class Other(object):
    def __init__(self, original):
        self._original = original
        self._category = Defs.Other

    @staticmethod
    def is_parsed():
        return False

    def get_original(self):
        return self._original

    def get_category(self):
        return self._category


def main():
    with open('Others.txt', 'r') as file:
        for line in file.readlines():
            print()
            print(line.strip())
            b = Parser.decode(line)
            if b.get_category() == Defs.OnLineJournal:
                print(b.get_category())
                print("Authors: ", end="")
                for item in b.get_authors():
                    print(item, end="  ")
                print("\nYear: " + b.get_year())
                print("Title: " + b.get_title())
                print("Journal: " + b.get_journal())
                print("Source: " + b.get_source())
                print()
            if b.get_category() == Defs.Website:
                print(b.get_category())
                print("Authors: ", end="")
                for item in b.get_authors():
                    print(item, end="  ")
                print("Year: " + b.get_year())
                print("Title: " + b.get_title())
                print("Source: " + b.get_source())
                print()
            if b.get_category() == Defs.Other:
                print(b.get_original())


if __name__ == "__main__":
    main()

