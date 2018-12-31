from Reference import Reference
import re
import Defs
import Parser


class Journal(Reference):
    def __init__(self, original):
        Reference.__init__(self, original)


class JournalPublished(Journal):
    def __init__(self, original):
        Journal.__init__(self, original)
        self._category = Defs.JournalPublished

    def get_category(self):
        return self._category

    def _parse_title(self):
        if re.search('.*[\.\?!]', self._get_body()):

            # if ends with .
            if re.search('.*?\D\.\s', self._get_body()):
                try:
                    self._title = re.search('(.*?\D)\.\s', self._get_body()).group(1).strip()
                    if len(self._title) == 0:
                        self._parsed = False
                        self._title = "error in title"
                except AttributeError:
                    self._parsed = False
                    self._title = "error in title"
            # elif, ends with ?
            elif re.search("\?", self._get_body()):
                try:
                    self._title = re.search('(.*?\?)\s', self._get_body()).group(1).strip()
                    if len(self._title) == 0:
                        self._parsed = False
                        self._title = "error in title"
                except AttributeError:
                    self._parsed = False
                    self._title = "error in title"

            # else, ends with !
            else:
                try:
                    self._title = re.search('(.*?!)\s', self._get_body()).group(1).strip()
                    if len(self._title) == 0:
                        self._parsed = False
                        self._title = "error in title"
                except AttributeError:
                    self._parsed = False
                    self._title = "error in title"
        else:
            self._parsed = False
            self._title = "error in title"

    def get_title(self):
        self._parse_title()
        return self._title

    def _parse_journal(self):
        exp = re.sub("\?", '.', self._get_body())
        exp = re.sub("!", '.', exp)
        try:
            self._journal = re.search(".*\.(.*?),\s\d.*", exp).group(1).strip()
            if len(self._journal) == 0:
                self._parsed = False
                self._title = "error in journal"
        except AttributeError:
            self._parsed = False
            self._journal = "error in journal"

    def get_journal(self):
        self._parse_journal()
        return self._journal

    def _parse_volume(self):
        if re.search('.*,.*\d+.*,', self._get_body()):
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

    def get_volume(self):
        self._parse_volume()
        return self._volume

    def get_issue(self):
        self._parse_volume()
        return self._issue

    def _parse_page_number(self):
        try:
            self._pages = re.findall('\w*\d+', re.search('.*,(.*?\d.*?)\.', self._get_body()).group(1))
            if len(self._pages) == 1:
                self._parsed = False
                self._pages = [self._pages[0], "error in ending page"]
        except AttributeError:
            self._parsed = False
            self._pages = ["error in beginning page", "error in ending page"]

    def get_start_page(self):
        self._parse_page_number()
        return self._pages[0]

    def get_end_page(self):
        self._parse_page_number()
        return self._pages[1]


class JournalInPress(Journal):
    def __init__(self, original):
        Journal.__init__(self, original)
        self._category = Defs.JournalInPress

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


def main():
    with open('Journal.txt', 'r') as file:
        for line in file.readlines():
            print(line.strip())
            b = Parser.decode(line)
            if b.get_category() == Defs.JournalPublished:
                print(b.get_category())
                print("Authors: ", end="")
                for item in b.get_authors():
                    print(item, end="  ")
                print("\nYear: " + b.get_year())
                print("Title: " + b.get_title())
                print("Journal: " + b.get_journal())
                print("Volume Number: " + b.get_volume())
                print("Issue Number: " + b.get_issue())
                print("Page Number: " + b.get_start_page() + " to " + b.get_end_page())
                print()
            if b.get_category() == Defs.JournalInPress:
                print(b.get_original().strip())
                print(b.get_category())
                print("Authors: ", end="")
                for item in b.get_authors():
                    print(item, end="  ")
                print("\nYear: " + b.get_year())
                print("Title: " + b.get_title())
                print("Journal: " + b.get_journal())
                print()


if __name__ == "__main__":
    main()
