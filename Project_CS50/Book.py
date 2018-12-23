import re
from Reference import Reference
import Transfer
import Defs

class Book(Reference):
    def __init__(self, original):
        Reference.__init__(self, original)

    def _parseTitle(self):
        if re.search('.*?\(.*?\)\.\s*(.*?)\.\s.*?', self._original):
            self._title = re.search('.*?\(.*?\)\.\s*(.*)\.\s.+', self._original).group(1).strip()
        else:
            self._parsed = False
            self._title = "error in book title"

    def getTitle(self):
        self._parseTitle()
        return self._title


class BookPublished(Book):
    def __init__(self, original):
        Book.__init__(self, original)
        # self._category = 'BookPublished'
        self._category = Defs.BookPublished

    def getCategory(self):
        return self._category

    def _parseLocation(self):
        if re.search('.*\.(.+):', self._original):
            location = re.search('.*\.(.+,.+):', self._original).group(1).strip()
            self._city = location.split(',')[0].strip()
            self._state = location.split(',')[-1].strip()
        else:
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
        if re.search('.*:(.+)\.', self._original):
            self._publisher = re.search('.*:(.+)\.', self._original).group(1).strip()
        else:
            self._parsed = False
            self._publisher = "error in publisher"

    def getPublisher(self):
        self._parsePublisher()
        return self._publisher

class BookInPress(Book):
    def __init__(self, original):
        Book.__init__(self, original)
        # self._category = "BookInPress"
        self._category = Defs.BookInPress

    def getCategory(self):
        return self._category


class BookOnline(Book):
    def __init__(self, original):
        Book.__init__(self, original)
        # self._category = "BookOnLine"
        self._category = Defs.BookOnLine

    def getCategory(self):
        return self._category

    def _parseSource(self):
        if re.search('[Rr]etrieved\sfrom', self._original):
            self._source = ['Webpage', re.search('[Rr]etrieved\sfrom(.*)', self._original).group(1).strip()]
        elif re.search('[(?:DOI)|(?:doi)]', self._original):
            self._source = ['DOI', re.search('[(?:DOI)|(?:doi)]:(.*)', self._original).group(1).strip()]
        else:
            self._parsed = False
            self._source = "error in source"

    def getSource(self):
        self._parseSource()
        return self._source
import Transfer
def main():
    with open('Book.txt', 'r') as file:
        for line in file.readlines():
            b = BookPublished(line)
            print(line.strip())
            print(b.getCategory())
            print(Transfer.BookPublished2AMJ(b))
            '''
            print("Authors: ", end="")
            for item in b.getAuthors():
                print(item, end="  ")
            print("\nYear: " + b.getYear())
            print("Title: " + b.getTitle())
            print("City: " + b.getCity())
            print("State: " + b.getState())
            print("Publisher: " + b.getPublisher())
            '''
            print()


if __name__ == "__main__":
    main()
