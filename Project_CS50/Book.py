import re
from Reference import Reference
import Defs


class Book(Reference):
    def __init__(self, original):
        Reference.__init__(self, original)

    def _parseTitle(self):
        try:
            self._title = re.search('.*?\(.*?\)\.\s*(.*)\.\s.+', self._original).group(1).strip()
        except AttributeError:
            self._parsed = False
            self._title = "error in book title"

    def getTitle(self):
        self._parseTitle()
        return self._title


class BookPublished(Book):
    def __init__(self, original):
        Book.__init__(self, original)
        self._category = Defs.BookPublished

    def getCategory(self):
        return self._category

    def _parseLocation(self):
        try:
            location = re.search('.*\.(.+,.+):', self._original).group(1).strip()
            self._city = location.split(',')[0].strip()
            self._state = location.split(',')[-1].strip()
        except AttributeError:
            self._parsed = False
            self._city = "error in city"
            self._state = "error in state"

    def getCity(self):
        self._parseLocation()
        return self._city

    def getState(self):
        self._parseLocation()
        return self._state

    def _parsePublisher(self):
        try:
            exp = self.getState() + ":(.+)\."
            self._publisher = re.search(exp, self._original).group(1).strip()
        except AttributeError:
            self._parsed = False
            self._publisher = "error in publisher"

    def getPublisher(self):
        self._parsePublisher()
        return self._publisher


class BookInPress(Book):
    def __init__(self, original):
        Book.__init__(self, original)
        self._category = Defs.BookInPress

    def getCategory(self):
        return self._category


class BookOnline(Book):
    def __init__(self, original):
        Book.__init__(self, original)
        self._category = Defs.BookOnLine

    def getCategory(self):
        return self._category

    def _parseSource(self):
        if re.search('[Rr]etrieved\sfrom', self._original):
            try:
                self._source = ['Webpage', re.search('[Rr]etrieved\sfrom(.*)', self._original).group(1).strip()]
            except AttributeError:
                self._parsed = False
                self._source = "error in source"
        elif re.search('[(?:DOI)|(?:doi)]', self._original):
            try:
                self._source = ['DOI', re.search('[(?:DOI)|(?:doi)]:(.*)', self._original).group(1).strip()]
            except AttributeError:
                self._parsed = False
                self._source = "error in source"
        else:
            self._parsed = False
            self._source = "error in source"

    def getSource(self):
        self._parseSource()
        return self._source


def main():
    with open('Book.txt', 'r') as file:
        for line in file.readlines():
            b = BookPublished(line)
            print(line.strip())
            print(b.getCategory())
            print("Authors: ", end="")
            for item in b.getAuthors():
                print(item, end="  ")
            print("\nYear: " + b.getYear())
            print("Title: " + b.getTitle())
            print("City: " + b.getCity())
            print("State: " + b.getState())
            print("Publisher: " + b.getPublisher())
            print()


if __name__ == "__main__":
    main()
