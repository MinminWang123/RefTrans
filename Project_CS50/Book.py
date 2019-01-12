"""
File: Book.py
Define BookPublished, BookInPress.
"""

import re
from Reference import Reference
import Defs
from Handler import *
import CodeBook


class Book(Reference):
    def __init__(self, original):
        Reference.__init__(self, original)


"""
class BookPublished
standard format: author(s) (year). title. location: publisher.
initialize:    BookPublished(str original)
get_category:  return Defs.BookPublished
get_original:  return str original
is_parsed:     return True if successfully parsed, False if any field fails
get_authors:   return a list of Author / str "error in author(s)"
get_year:      return str year / "error in year"
get_title:     return str book title / "error in title"
get_location:  return str location / "error in location"
get_publisher: return str publisher / "error in publisher"
get_source:    return str source if present, "" otherwise

encode_authors():   return Handler.authors
encode_year():      return Handler.general
encode_title():     return Handler.title
encode_location():  return Handler.general
encode_publisher(): return Handler.general
encode_source():    return Handler.general
encode()
"""


class BookPublished(Book):
    def __init__(self, original):
        Book.__init__(self, original)
        self._category = Defs.BookPublished

    def get_category(self):
        return self._category

    def _parse_title(self):
        self._title = ""
        try:
            self._title = re.search(r'(.*)\.\s?.+', self._get_body()).group(1).strip()
            if len(self._title) == 0:
                self._parsed = False
                self._title = "error in book title"
        except AttributeError:
            self._parsed = False
            self._title = "error in book title"

    def get_title(self):
        self._parse_title()
        return self._title

    def encode_title(self, dic):
        return Handler.title(self.get_title(), dic)

    def _parse_location(self):
        self._location = ""
        try:
            self._location = re.search(r'.*\.(.+):', self._get_body()).group(1).strip()
            if len(self._location) == 0:
                self._parsed = False
                self._location = "error in location"
        except AttributeError:
            self._parsed = False
            self._location = "error in location"

    def get_location(self):
        self._parse_location()
        return self._location

    def encode_location(self, dic):
        return Handler.general(self.get_location(), dic)

    def _parse_publisher(self):
        self._publisher = ""
        self._parse_location()
        if self._location == "error in state":
            exp = r"\.:(.+?)\.$"
        else:
            exp = self.get_location() + r":(.+?)\.$"
        try:
            self._publisher = re.search(exp, self._get_body()).group(1).strip()
            if len(self._publisher) == 0:
                self._parsed = False
                self._publisher = "error in publisher"
        except AttributeError:
            self._parsed = False
            self._publisher = "error in publisher"

    def get_publisher(self):
        self._parse_publisher()
        return self._publisher

    def encode_publisher(self, dic):
        return Handler.general(self.get_publisher(), dic)

    def encode(self, codebook):

        # seq: location publisher
        if codebook["BookPublished"]["seq"] == "lopu":
            return self.encode_authors(codebook["authors"]) + self.encode_year(codebook["year"]) \
               + self.encode_title(codebook["BookPublished"]["title"]) \
               + self.encode_location(codebook["BookPublished"]["location"]) \
               + self.encode_publisher(codebook["BookPublished"]["publisher"])

        # seq: publisher location
        elif codebook["BookPublished"]["seq"] == "pulo":
            return self.encode_authors(codebook["authors"]) + self.encode_year(codebook["year"]) \
               + self.encode_title(codebook["BookPublished"]["title"]) \
               + self.encode_publisher(codebook["BookPublished"]["publisher"]) \
               + self.encode_location(codebook["BookPublished"]["location"])



"""
class BookInPress
standard format: author(s) (in press). title. source
initialize:    BookInPress(str original)
get_category:  return Defs.BookInPress
get_original:  return str original
is_parsed:     return True if successfully parsed, False if any field fails
get_authors:   return a list of Author / str "error in author(s)"
get_year:      return str year / "error in year"
get_title:     return str book title / "error in title"
get_source:    return str source if present, "" otherwise

encode_authors():   return Handler.authors
encode_year():      return Handler.general
encode_title():     return Handler.title
encode_source():    return Handler.general
encode()
"""


class BookInPress(Book):
    def __init__(self, original):
        Book.__init__(self, original)
        self._category = Defs.BookInPress

    def get_category(self):
        return self._category

    def _parse_title(self):
        self._title = ""
        self._title = self._get_body().strip().strip(".")
        if len(self._title) == 0:
            self._parsed = False
            self._title = "error in book title"

    def get_title(self):
        self._parse_title()
        return self._title

    def encode_title(self, dic):
        return Handler.title(self.get_title(), dic)

    def encode(self, codebook):
        return self.encode_authors(codebook["authors"]) + self.encode_year(codebook["year"]) \
               + self.encode_title(codebook["BookInPress"]["title"])


def main():
    # with open('test_cases/BookPublished.txt', 'r') as file:
    #     for line in file.readlines():
    #         b = BookPublished(line)
    #         print(line.strip())
    #         print(b.encode_authors(char_end=""))
    #         print(b.encode_year())
    #         print(b.encode_title(head='"', tail='"', bold=True))
    #         print(b.encode_location())
    #         print(b.encode_publisher())
            # print(b.get_category())
            # print("Authors: ", end="")
            # for item in b.get_authors():
            #     print(item, end="  ")
            # print("\nYear: " + b.get_year())
            # print("Title: " + b.get_title())
            # print("Location: " + b.get_location())
            # print("Publisher: " + b.get_publisher())
            # print()
    text = "Aiken, L. S., & West, S. G. (1991). Multiple regression: Testing and interpreting interactions. Newbury Park, CA: Sage."
    ref = BookPublished(text)
    print(ref.encode(CodeBook.AMJ))
    text1 = "Aiken, L. S., & West, S. G. (in press). Multiple regression: Testing and interpreting interactions."
    ref1 = BookInPress(text1)
    print(ref1.encode(CodeBook.AMJ))

if __name__ == "__main__":
    main()