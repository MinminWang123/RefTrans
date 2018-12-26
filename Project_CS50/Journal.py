from Reference import Reference
import re
import Defs


class Journal(Reference):
    def __init__(self, original):
        Reference.__init__(self, original)

    def _parseTitle(self):
        if re.search('.*?\)\..*\.|\?', self._original):
            if re.search('.*?\)\..*?\D\.\s', self._original):
                try:
                    self._title = re.search('.*?\)\.(.*?\D)\.\s', self._original).group(1).strip()
                except AttributeError:
                    self._parsed = False
                    self._title = "error in title"
            else:
                try:
                    self._title = re.search('.*?\)\.(.*?\?)\s', self._original).group(1).strip()
                except AttributeError:
                    self._parsed = False
                    self._title = "error in title"
        else:
            self._parsed = False
            self._title = "error in title"

    def getTitle(self):
        self._parseTitle()
        return self._title


class JournalPublished(Journal):
    def __init__(self, original):
        Journal.__init__(self, original)
        self._category = Defs.JournalPublished

    def getCategory(self):
        return self._category

    def _parseJournal(self):
        exp = re.sub("\(", '\(', self.getTitle())
        exp = re.sub("\)", '\)', exp)
        exp = re.sub("\?", '\?', exp) + "\.*(.*?),\s\d+"
        try:
            self._journal = re.search(exp, self._original).group(1).strip()
        except AttributeError:
            self._parsed = False
            self._journal = "error in journal"

    def getJournal(self):
        self._parseJournal()
        return self._journal

    def _parseVolume(self):
        if re.search('.*,.*\d+.*,', self._original):
            try:
                volume = re.search('.*,(.*\d+.*),', self._original).group(1).strip()
                if re.search('.*\(.*\)', volume):
                    self._volume = re.search('(.*)\((.*)\)', volume).group(1).strip()
                    self._issue = re.search('(.*)\((.*)\)', volume).group(2).strip()
                else:
                    self._volume = volume
                    self._issue = ""
            except AttributeError:
                self._parsed = False
                self._volume = "error in volume number"
                self._issue = "error in issue number"

        else:
            self._parsed = False
            self._volume = "error in volume number"
            self._issue = "error in issue number"

    def getVolume(self):
        self._parseVolume()
        return self._volume

    def getIssue(self):
        self._parseVolume()
        return self._issue

    def _parsePageNumber(self):
        try:
            self._pages = re.findall('\w*\d+', re.search('.*,(.*?\d.*?)\.', self._original).group(1))
        except AttributeError:
            self._parsed = False
            self._pages = ["error in page number", "error in page number"]

    def getStartPage(self):
        self._parsePageNumber()
        return self._pages[0]

    def getEndPage(self):
        self._parsePageNumber()
        return self._pages[1]

    def _parseSource(self):
        try:
            exp = self.getEndPage() + "\.\s*(\w+.*)"
            self._source = re.search(exp, self._original).group(1).strip()
        except AttributeError:
            self._source = ""

    def getSource(self):
        self._parseSource()
        return self._source


class JournalInPress(Journal):
    def __init__(self, original):
        Journal.__init__(self, original)
        self._category = Defs.JournalInPress

    def getCategory(self):
        return self._category

    def _parseJournal(self):
        exp = re.sub("\(", '\(', self.getTitle())
        exp = re.sub("\)", '\)', exp)
        exp = re.sub("\?", '\?', exp) + "\.*(.*?)\."
        try:
            self._journal = re.search(exp, self._original).group(1).strip()
        except AttributeError:
            self._parsed = False
            self._journal = "error in journal"

    def getJournal(self):
        self._parseJournal()
        return self._journal


class JournalOnLine(Journal):
    def __init__(self, original):
        Journal.__init__(self, original)
        self._category = Defs.JournalOnLine

    def getCategory(self):
        return self._category


def main():
    with open('Journal.txt', 'r') as file:
        for line in file.readlines():
            b = JournalPublished(line)
            print(line.strip())
            print("Authors: ", end="")
            for item in b.getAuthors():
                print(item, end="  ")
            print("\nYear: " + b.getYear())
            print("Title: " + b.getTitle())
            print("Journal: " + b.getJournal())
            print("Volume Number: " + b.getVolume())
            print("Issue Number: " + b.getIssue())
            print("Page Number: " + b.getStartPage() + " to " + b.getEndPage())
            print("Source: " + b.getSource())
            print()


if __name__ == "__main__":
    main()
