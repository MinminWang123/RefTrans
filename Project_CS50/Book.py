import re
from Reference import Reference
import Defs
import Parser


class Book(Reference):
    def __init__(self, original):
        Reference.__init__(self, original)


class BookPublished(Book):
    def __init__(self, original):
        Book.__init__(self, original)
        self._category = Defs.BookPublished

    def get_category(self):
        return self._category

    def _parse_title(self):
        try:
            self._title = re.search('(.*)\.\s?.+', self._get_body()).group(1).strip()
            if len(self._title) == 0:
                self._parsed = False
                self._title = "error in book title"
        except AttributeError:
            self._parsed = False
            self._title = "error in book title"

    def get_title(self):
        self._parse_title()
        return self._title

    def _parse_location(self):
        try:
            self._location = re.search('.*\.(.+):', self._get_body()).group(1).strip()
            if len(self._location) == 0:
                self._parsed = False
                self._location = "error in location"
        except AttributeError:
            self._parsed = False
            self._location = "error in location"

    def get_location(self):
        self._parse_location()
        return self._location

    def _parse_publisher(self):
        self._parse_location()
        if self._location == "error in state":
            exp = "\.:(.+?)\.$"
        else:
            exp = self.get_location() + ":(.+?)\.$"
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


class BookInPress(Book):
    def __init__(self, original):
        Book.__init__(self, original)
        self._category = Defs.BookInPress

    def get_category(self):
        return self._category

    def _parse_title(self):
        self._title = self._get_body().strip(".")
        if len(self._title) == 0:
            self._parsed = False
            self._title = "error in book title"

    def get_title(self):
        self._parse_title()
        return self._title


def main():
    with open('Book.txt', 'r') as file:
        for line in file.readlines():
            b = Parser.decode(line)
            print(line.strip())
            print(b.get_category())
            if b.get_category() == Defs.BookPublished:
                # print("Authors: ", end="")
                # for item in b.get_authors():
                #     print(item, end="  ")
                # print("\nYear: " + b.get_year())
                # print("Title: " + b.get_title())
                # print("Location: " + b.get_location())
                # print("Publisher: " + b.get_publisher())
                print()
            if b.get_category() == Defs.BookInPress:
                # print("Authors: ", end="")
                # for item in b.get_authors():
                #     print(item, end="  ")
                # print("\nYear: " + b.get_year())
                # print("Title: " + b.get_title())
                print()


if __name__ == "__main__":
    main()
