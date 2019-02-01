"""
File: Chapter.py
Define ChapterPublished, ChapterInPress
"""


from Reference import Reference
import re
from Author import AuthorFL
import Defs
from Handler import *


class Chapter(Reference):
    def __init__(self, original):
        Reference.__init__(self, original)

    def _parse_chapter_title(self):
        self._ctitle = ""
        try:
            self._ctitle = re.search(r'(.*?)[\.\?]\sIn.+', self._get_body()).group(1).strip()
            if len(self._ctitle) == 0:
                self._parsed = False
                self._ctitle = "error in chapter title"
        except AttributeError:
            self._parsed = False
            self._ctitle = "error in chapter title"

    def get_chapter_title(self):
        self._parse_chapter_title()
        return self._ctitle

    def encode_chapter_title(self, dic):
        return Handler.title(self.get_chapter_title(), dic)

    def _parse_editors(self):
        self._editors = []
        try:
            self._split_editors(re.search(r'.*In\s(.*?)\([Ee]ds*.*\)', self._original).group(1).strip())
        except AttributeError:
            self._parsed = False
            self._editors = "error in editor(s)"

    def _split_editors(self, raw_text):
        editors = re.findall(r'(?:[A-Z]\.\s*)+(?:\w|\s)+', raw_text)
        if len(editors) == 0:
            self._parsed = False
            self._editors = "error in editor(s)"
            return
        for editor in editors:
            self._editors.append(AuthorFL(editor))

    def get_editors(self):
        self._parse_editors()
        return self._editors

    def encode_editors(self, dic):
        return Handler.editors(self.get_editors(), dic)


"""
class ChapterPublished
standard format: author(s) (year). chapter title. In editors (Ed./Eds.), 
                 book title ((page addition, )pp. page-page). location: publisher
initialize:        ChapterPublished(str original)
get_category:      return Defs.ChapterPublished
get_original:      return str original
is_parsed:         return True if successfully parsed, False if any field fails
get_authors:       return a list of Author / str "error in author(s)"
get_year:          return str year / "error in year"
get_chapter_title: return str chapter title / "error in chapter title"
get_editors:       return a list of Author / str "error in editor(s)"
get_book_title:    return str book title / "error in book title"
get_start_page:    return str start page / "error in starting page"
get_end_page:      return str end page / "error in ending page"
get_page_addition: return str page addition if present, "" otherwise
get_location:      return str location / "error in location"
get_publisher:     return str publisher / "error in publisher"
get_source:        return str source if present, "" otherwise

encode_authors():       return Handler.authors
encode_year():          return Handler.general
encode_chapter_title(): return Handler.title
encode_editors():       return Handler.editors
encode_book_title():    return Handler.title
encode_pages():         return Handler.pages
encode_page_addition(): return Handler.page_addition
encode_location():      return Handler.general
encode_publisher():     return Handler.general
encode_source():        return Handler.general
encode()
"""


class ChapterPublished(Chapter):
    def __init__(self, original):
        Chapter.__init__(self, original)
        self._category = Defs.ChapterPublished

    def get_category(self):
        return self._category

    def _parse_book_title(self):
        self._btitle = ""
        try:
            self._btitle = re.search(r'\([Ee]ds*.*\).*?(\w.*?)\(.*pp', self._original).group(1).strip()
            if len(self._btitle) == 0:
                self._parsed = False
                self._btitle = "error in book title"
        except AttributeError:
            self._parsed = False
            self._btitle = "error in book title"

    def get_book_title(self):
        self._parse_book_title()
        return self._btitle

    def encode_book_title(self, dic):
        return Handler.title(self.get_book_title(), dic)

    def _parse_page_number(self):
        self._pages = ["", ""]
        self._page_addition = ""
        try:
            self._page_addition = re.search(r'.*\((.*?)pp(.*?)\)', self._original).group(1)
            self._pages = re.findall(r'\w*\d+', re.search(r'.*\(.*?pp(.*?)\)', self._original).group(1))
            if len(self._pages) == 1:
                self._parsed = False
                self._pages = [self._pages[0], "error in ending page"]
        except AttributeError:
            self._parsed = False
            self._page_addition = ""
            self._pages = ["error in starting page", "error in ending page"]

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

    def encode_pages(self, dic):
        return Handler.pages(self.get_start_page(), self.get_end_page(), dic)

    def encode_page_addition(self, dic):
        return Handler.page_addition(self.get_page_addition(), dic)

    def _parse_location(self):
        self._location = ""
        try:
            self._location = re.search(r'.*\.(.+):.*', self._get_body()).group(1).strip()
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
        if self._location == "error in location":
            exp = r"\.\s:(.+)\."
        else:
            exp = self.get_location() + r":(.+)\."
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
        if codebook["ChapterPublished"]["seq"] == "palo":
            return self.encode_authors(codebook["authors"]) + self.encode_year(codebook["year"]) \
                   + self.encode_chapter_title(codebook["ChapterPublished"]["chapter_title"]) \
                   + self.encode_editors(codebook["ChapterPublished"]["editors"]) \
                   + self.encode_book_title(codebook["ChapterPublished"]["book_title"]) \
                   + self.encode_page_addition(codebook["ChapterPublished"]["page_addition"]) \
                   + self.encode_pages(codebook["ChapterPublished"]["pages"]) \
                   + self.encode_location(codebook["ChapterPublished"]["location"]) \
                   + self.encode_publisher(codebook["ChapterPublished"]["publisher"])
        elif codebook["ChapterPublished"]["seq"] == "lopa":
            return self.encode_authors(codebook["authors"]) + self.encode_year(codebook["year"]) \
                   + self.encode_chapter_title(codebook["ChapterPublished"]["chapter_title"]) \
                   + self.encode_editors(codebook["ChapterPublished"]["editors"]) \
                   + self.encode_book_title(codebook["ChapterPublished"]["book_title"]) \
                   + self.encode_location(codebook["ChapterPublished"]["location"]) \
                   + self.encode_publisher(codebook["ChapterPublished"]["publisher"]) \
                   + self.encode_page_addition(codebook["ChapterPublished"]["page_addition"]) \
                   + self.encode_pages(codebook["ChapterPublished"]["pages"])


"""
class ChapterInPress
standard format: author(s) (in press). chapter title. In editors (Ed./Eds.), book title.
initialize:        ChapterInPress(str original)
get_category:      return Defs.ChapterInPress
get_original:      return str original
is_parsed:         return True if successfully parsed, False if any field fails
get_authors:       return a list of Author / str "error in author(s)"
get_year:          return str year / "error in year"
get_chapter_title: return str chapter title / "error in chapter title"
get_editors:       return a list of Author / str "error in editor(s)"
get_book_title:    return str book title / "error in book title"
get_source:        return str source if present, "" otherwise

encode_authors():       return Handler.authors
encode_year():          return Handler.general
encode_chapter_title(): return Handler.title
encode_editors():       return Handler.editors
encode_book_title():    return Handler.title
encode_source():        return Handler.general
encode()
"""


class ChapterInPress(Chapter):
    def __init__(self, original):
        Chapter.__init__(self, original)
        self._category = Defs.ChapterInPress

    def get_category(self):
        return self._category

    def _parse_book_title(self):
        self._btitle = ""
        try:
            self._btitle = re.search(r'\([Ee]ds*.*\).*?(\w.*?)\.', self._get_body()).group(1).strip()
            if len(self._btitle) == 0:
                self._parsed = False
                self._btitle = "error in book title"
        except AttributeError:
            self._parsed = False
            self._btitle = "error in book title"

    def get_book_title(self):
        self._parse_book_title()
        return self._btitle

    def encode_book_title(self, dic):
        return Handler.title(self.get_book_title(), dic)

    def encode(self, codebook):
        return self.encode_authors(codebook["authors"]) + self.encode_year(codebook["year"]) \
               + self.encode_chapter_title(codebook["ChapterInPress"]["chapter_title"]) \
               + self.encode_editors(codebook["ChapterInPress"]["editors"]) \
               + self.encode_book_title(codebook["ChapterInPress"]["book_title"]) \
               + self.encode_source(codebook["ChapterInPress"]["doi"])


def main():
    # with open('test_cases/ChapterPublished.txt', 'r') as file:
    #     for line in file.readlines():
    #         print(line.strip())
    #         b = ChapterPublished(line)
    #         print(b.encode_authors())
    #         print(b.encode_year())
    #         print(b.encode_chapter_title())
    #         if len(b.get_editors()) <= 1:
    #             print(b.encode_editors(head="in ", tail="(ed)"))
    #         else:
    #             print(b.encode_editors(head="in ", tail="(eds)"))
    #         print(b.encode_book_title())
    #         print(b.encode_pages())
    #         print(b.encode_location())
    #         print(b.encode_publisher())
    #         print()
            # if b.get_category() == Defs.ChapterPublished:
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
                # print()
            # if b.get_category() == Defs.ChapterInPress:
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
                # print()
    text = "Chen, G., Mathieu, J. E., & Bliese, P. D. (2004). A framework for conducting multilevel construct validation. In F. J. Yammarino & F. Dansereau (Eds.), Research in multilevel issues: Multilevel issues in organizational behavior and processes (Vol. 3, pp. 273–303). Oxford, UK: Elsevier."
    ref = ChapterPublished(text)
    print(ref.encode(CodeBook.AMJ))
    text1 = "Chen, G., Mathieu, J. E., & Bliese, P. D. (2004). A framework for conducting multilevel construct validation. In F. J. Yammarino & F. Dansereau (Eds.), Research in multilevel issues: Multilevel issues in organizational behavior and processes."
    ref1 = ChapterInPress(text1)
    print(ref1.encode(CodeBook.AMJ))


if __name__ == "__main__":
    main()
