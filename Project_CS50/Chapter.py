from Reference import Reference
import re
from Author import AuthorFL


class Chapter(Reference):
    def __init__(self, original):
        Reference.__init__(self, original)
        self._ctitle = ""
        self._editors = []

    def _parseChapterTitle(self):
        if re.search('.*?\(.*?\)\.\s*(.*?)\.\sIn.*?', self._original):
            self._ctitle = re.search('.*?\(.*?\)\.\s*(.*?)\.\sIn.+', self._original).group(1).strip()
        else:
            self._parsed = False
            self._ctitle = "error in chapter title"

    def getChapterTitle(self):
        self._parseChapterTitle()
        return self._ctitle

    def _parseEditors(self):
        if re.search('.*In\s(.*?)\([Ee]ds*.*\)', self._original):
            self._splitEditors(re.search('.*In\s(.*?)\([Ee]ds*.*\)', self._original).group(1).strip())
        else:
            self._parsed = False
            self._editors = "error in editors"

    def _splitEditors(self, rawText):
        editors = re.findall('(?:[A-Z]\.\s*)+(?:\w|\s)+', rawText)
        for editor in editors:
            self._editors.append(AuthorFL(editor))

    def getEditors(self):
        self._parseEditors()
        return self._editors


class ChapterPublished(Chapter):
    def __init__(self, original):
        Chapter.__init__(self, original)
        self._category = 'ChapterPublished'

    def getCategory(self):
        return self._category

    def _parseBookTitle(self):
        if re.search('\([Ee]ds*.*\).*?\w+.*?\(.*pp', self._original):
            self._btitle = re.search('\([Ee]ds*.*\).*?(\w.*?)\(.*pp', self._original).group(1).strip()
        else:
            self._parsed = False
            self._btitle = "error in book title"

    def getBookTitle(self):
        self._parseBookTitle()
        return self._btitle

    def _parsePageNumber(self):
        if re.search('.*\(.*?pp.*?\)', self._original):
            self._pageAddition = re.search('.*\((.*?)pp(.*?)\)', self._original).group(1)
            self._pages = re.findall('\w*\d+', re.search('.*\(.*?pp(.*?)\)', self._original).group(1))
        else:
            self._parsed = False
            self._pages = ["error in page number", "error in page number"]

    def getStartPage(self):
        self._parsePageNumber()
        return self._pages[0]

    def getEndPage(self):
        self._parsePageNumber()
        return self._pages[1]

    def getPageAddition(self):
        self._parsePageNumber()
        if self._pageAddition:
            self._pageAddition = self._pageAddition.split(",")[0]
        return self._pageAddition

    def _parseLocation(self):
        if re.search('.*pp.*\)\.*.*:.*', self._original):
            location = re.search('.*pp.*\)\.*(.+,.+?):.*', self._original).group(1).strip()
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
        exp = self.getState() + ":(.+)\.\s.*"
        if re.search(exp, self._original):
            self._publisher = re.search(exp, self._original).group(1).strip()
        else:
            self._parsed = False
            self._publisher = "error in publisher"

    def getPublisher(self):
        self._parsePublisher()
        return self._publisher

    def _parseSource(self):
        exp = self.getPublisher() + ".*?(\w+.*)"
        if re.search(exp, self._original):
            self._source = re.search(exp, self._original).group(1).strip()
        else:
            self._source = ""

    def getSource(self):
        self._parseSource()
        return self._source


class ChapterInPress(Chapter):
    def __init__(self, original):
        Chapter.__init__(self, original)
        self._category = "ChapterInPress"

    def getCategory(self):
        return self._category


class ChapterOnline(Chapter):
    def __init__(self, original):
        Chapter.__init__(self, original)
        self._category = "ChapterOnline"

    def getCategory(self):
        return self._category

import Transfer
def main():
    with open('Chapter.txt', 'r') as file:
        for line in file.readlines():
            b = ChapterPublished(line)
            print(line.strip())
            '''
            print("Authors: ", end="")
            for item in b.getAuthors():
                print(item, end="  ")
            print("\nYear: " + b.getYear())
            print("Chapter Title: " + b.getChapterTitle())
            print("Editors: ", end="")
            for item in b.getEditors():
                print(item, end="  ")
            print("\nBook Title: " + b.getBookTitle())
            print("Page Number: " + b.getStartPage() + " to " + b.getEndPage())
            print("Page Addition: " + b.getPageAddition())
            print("City: " + b.getCity())
            print("State: " + b.getState())
            print("Publisher: " + b.getPublisher())
            print("Source: " + b.getSource())
            '''
            print()
            print(Transfer.ChapterPublished2AMJ(b))


if __name__ == "__main__":
    main()
