from Reference import Reference
import re
from Author import AuthorFL
import Defs
import Parser


class Chapter(Reference):
    def __init__(self, original):
        Reference.__init__(self, original)
        self._ctitle = ""
        self._editors = []

    def _parse_chapter_title(self):
        try:
             self._ctitle = re.search('(.*?)[\.\?]\sIn.+', self._get_body()).group(1).strip()
        except AttributeError:
            self._parsed = False
            self._ctitle = "error in chapter title"

    def get_chapter_title(self):
        self._parse_chapter_title()
        return self._ctitle

    def _parse_editors(self):
        try:
            self._split_editors(re.search('.*In\s(.*?)\([Ee]ds*.*\)', self._original).group(1).strip())
        except AttributeError:
            self._parsed = False
            self._editors = "error in editors"

    def _split_editors(self, raw_text):
        editors = re.findall('(?:[A-Z]\.\s*)+(?:\w|\s)+', raw_text)
        for editor in editors:
            self._editors.append(AuthorFL(editor))

    def get_editors(self):
        self._parse_editors()
        return self._editors


class ChapterPublished(Chapter):
    def __init__(self, original):
        Chapter.__init__(self, original)
        self._category = Defs.ChapterPublished

    def get_category(self):
        return self._category

    def _parse_book_title(self):
        try:
            self._btitle = re.search('\([Ee]ds*.*\).*?(\w.*?)\(.*pp', self._original).group(1).strip()
        except AttributeError:
            self._parsed = False
            self._btitle = "error in book title"

    def get_book_title(self):
        self._parse_book_title()
        return self._btitle

    def _parse_page_number(self):
        try:
            self._page_addition = re.search('.*\((.*?)pp(.*?)\)', self._original).group(1)
            self._pages = re.findall('\w*\d+', re.search('.*\(.*?pp(.*?)\)', self._original).group(1))
        except AttributeError:
            self._parsed = False
            self._page_addition = None
            self._pages = ["error in page number", "error in page number"]

    def get_start_page(self):
        self._parse_page_number()
        return self._pages[0]

    def get_end_page(self):
        self._parse_page_number()
        return self._pages[1]

    def get_page_addition(self):
        self._parse_page_number()
        if self._page_addition:
            return self._page_addition.split(",")[0]
        return ""

    def _parse_location(self):
        try:
            self._location = re.search('.*\.(.+):.*', self._get_body()).group(1).strip()
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
        if self._location == "error in location":
            exp = "\.\s:(.+)\."
        else:
            exp = self.get_location() + ":(.+)\."
        try:
            self._publisher = re.search(exp, self._get_body()).group(1).strip()
        except AttributeError:
            self._parsed = False
            self._publisher = "error in publisher"

    def get_publisher(self):
        self._parse_publisher()
        return self._publisher


class ChapterInPress(Chapter):
    def __init__(self, original):
        Chapter.__init__(self, original)
        self._category = Defs.ChapterInPress

    def get_category(self):
        return self._category

    def _parse_book_title(self):
        try:
            self._btitle = re.search('\([Ee]ds*.*\).*?(\w.*?)\.', self._get_body()).group(1).strip()
        except AttributeError:
            self._parsed = False
            self._btitle = "error in book title"

    def get_book_title(self):
        self._parse_book_title()
        return self._btitle


def main():
    with open('Chapter.txt', 'r') as file:
        for line in file.readlines():
            print()
            print(line.strip())
            b = Parser.decode(line)
            if b.get_category() == Defs.ChapterPublished:
                # print(b.get_category())
                # print("Authors: ", end="")
                # for item in b.get_authors():
                #     print(item, end="  ")
                # print("\nYear: " + b.get_year())
                # print("Chapter Title: " + b.get_chapter_title())
                # print("Editors: ", end="")
                # for item in b.get_editors():
                #     print(item, end="  ")
                # print("\nBook Title: " + b.get_book_title())
                # print("Page Number: " + b.get_start_page() + " to " + b.get_end_page())
                # print("Page Addition: " + b.get_page_addition())
                # print("Location: " + b.get_location())
                # print("Publisher: " + b.get_publisher())
                print()
            if b.get_category() == Defs.ChapterInPress:
                # print(b.get_category())
                # print("Authors: ", end="")
                # for item in b.get_authors():
                #     print(item, end="  ")
                # print("\nYear: " + b.get_year())
                # print("Chapter Title: " + b.get_chapter_title())
                # print("Editors: ", end="")
                # for item in b.get_editors():
                #     print(item, end="  ")
                # print("\nBook Title: " + b.get_book_title())
                print()


if __name__ == "__main__":
    main()
