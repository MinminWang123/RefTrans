"""
File: Journal.py
Define JournalPublished, JournalInPress
"""


from Reference import Reference
import Defs
from Handler import *
import CodeBook


class Journal(Reference):
    def __init__(self, original):
        Reference.__init__(self, original)


"""
class JournalPublished
standard format: author(s) (year). title. journal, volume(issue), page-page.
initialize:     JournalPublished(str original)
get_category:   return Defs.JournalPublished
get_original:   return str original
is_parsed:      return True if successfully parsed, False if any field fails
get_authors:    return a list of Author / str "error in author(s)"
get_year:       return str year / "error in year"
get_title:      return str title("." excluded, "?" & "!" included) / "error in title"
get_journal:    return str journal / "error in journal"
get_volume:     return str volume number / "error in volume number"
get_issue:      return str issue number if present, "" otherwise
get_start_page: return str start page / "error in starting page"
get_end_page:   return str end page / "error in ending page"
get_source:     return str source if present, "" otherwise

encode_authors(): return Handler.authors
encode_year():    return Handler.general
encode_title():   return Handler.title
encode_journal(): return Handler.general
encode_volume():  return Handler.general
encode_issue():   return Handler.issue
encode_pages():   return Handler.pages
encode_source():  return Handler.general
encode()
"""


class JournalPublished(Journal):
    def __init__(self, original):
        Journal.__init__(self, original)
        self._category = Defs.JournalPublished

    def get_category(self):
        return self._category

    def _parse_title(self):
        if re.search(r'.*[\.\?!]', self._get_body()):

            # if ends with .
            if re.search(r'.*?\D\.\s', self._get_body()):
                try:
                    self._title = re.search('(.*?\D)\.\s', self._get_body()).group(1).strip()
                    if len(self._title) == 0:
                        self._parsed = False
                        self._title = "error in title"
                except AttributeError:
                    self._parsed = False
                    self._title = "error in title"

            # elif, ends with ?
            elif re.search(r"\?", self._get_body()):
                try:
                    self._title = re.search(r'(.*?\?)\s', self._get_body()).group(1).strip()
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

    def encode_title(self, dic):
        return Handler.title(self.get_title(), dic)

    def _parse_journal(self):
        exp = re.sub(r"\?", '.', self._get_body())
        exp = re.sub(r"!", '.', exp)
        try:
            self._journal = re.search(r".*\.(.*?),\s\d.*", exp).group(1).strip()
            if len(self._journal) == 0:
                self._parsed = False
                self._title = "error in journal"
        except AttributeError:
            self._parsed = False
            self._journal = "error in journal"

    def get_journal(self):
        self._parse_journal()
        return self._journal

    def encode_journal(self, dic):
        return Handler.general(self.get_journal(), dic)

    def _parse_volume(self):
        if re.search(r'.*,.*\d+.*,', self._get_body()):
            try:
                volume = re.search(r'.*,(.*\d+.*),', self._original).group(1).strip()
                if re.search(r'.*\(.*\)', volume):
                    self._volume = re.search(r'(.*)\((.*)\)', volume).group(1).strip()
                    self._issue = re.search(r'(.*)\((.*)\)', volume).group(2).strip()
                else:
                    self._volume = volume
                    self._issue = ""
            except AttributeError:
                self._parsed = False
                self._volume = "error in volume number"
                self._issue = ""

        else:
            self._parsed = False
            self._volume = "error in volume number"
            self._issue = ""

    def get_volume(self):
        self._parse_volume()
        return self._volume

    def get_issue(self):
        self._parse_volume()
        return self._issue

    def encode_volume(self, dic):
        return Handler.general(self.get_volume(), dic)

    def encode_issue(self, dic):
        return Handler.issue(self.get_issue(), dic)

    def _parse_page_number(self):
        try:
            self._pages = re.findall(r'\w*\d+', re.search(r'.*,(.*?\d.*?)\.', self._get_body()).group(1))
            if len(self._pages) == 1:
                self._parsed = False
                self._pages = [self._pages[0], "error in ending page"]
        except AttributeError:
            self._parsed = False
            self._pages = ["error in starting page", "error in ending page"]

    def get_start_page(self):
        self._parse_page_number()
        return self._pages[0]

    def get_end_page(self):
        self._parse_page_number()
        return self._pages[1]

    def encode_pages(self, dic):
        return Handler.pages(self.get_start_page(), self.get_end_page(), dic)

    def encode(self, codebook):
        return self.encode_authors(codebook["authors"]) + self.encode_year(codebook["year"]) \
               + self.encode_title(codebook["JournalPublished"]["title"]) \
               + self.encode_journal(codebook["JournalPublished"]["journal"]) \
               + self.encode_volume(codebook["JournalPublished"]["volume"]) \
               + self.encode_issue(codebook["JournalPublished"]["issue"]) \
               + self.encode_pages(codebook["JournalPublished"]["pages"])


"""
class JournalInPress
standard format: author(s) (in press). title. journal. source
initialize:     JournalInPress(str original)
get_category:   return Defs.JournalInPress
get_original:   return str original
is_parsed:      return True if successfully parsed, False if any field fails
get_authors:    return a list of Author / str "error in author(s)"
get_year:       return str year / "error in year"
get_title:      return str title("." excluded, "?" & "!" included) / "error in title"
get_journal:    return str journal / "error in journal"
get_source:     return str source if present, "" otherwise

encode_authors(): return Handler.authors
encode_year():    return Handler.general
encode_title():   return Handler.title
encode_journal(): return Handler.general
encode_source():  return Handler.general
encode()
"""


class JournalInPress(Journal):
    def __init__(self, original):
        Journal.__init__(self, original)
        self._category = Defs.JournalInPress

    def get_category(self):
        return self._category

    def _parse_title(self):
        self._parse_journal()
        if self.get_journal() == "error in journal":
            exp = r"^(.*)[\.\?\!]\s"
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
        return self._title.strip().strip(".")

    def encode_title(self, dic):
        return Handler.title(self.get_title(), dic)

    def _parse_journal(self):
        exp = re.sub("\?", '.', self._get_body())
        exp = re.sub("!", '.', exp)
        try:
            self._journal = re.search(r".*\.(.+?)\.", exp).group(1).strip()
            if len(self._journal) == 0:
                self._parsed = False
                self._journal = "error in journal"
        except AttributeError:
            self._parsed = False
            self._journal = "error in journal"

    def get_journal(self):
        self._parse_journal()
        return self._journal

    def encode_journal(self, dic):
        return Handler.general(self.get_journal(), dic)

    def encode(self, codebook):
        return self.encode_authors(codebook["authors"]) + self.encode_year(codebook["year"]) \
               + self.encode_title(codebook["JournalInPress"]["title"]) \
               + self.encode_journal(codebook["JournalInPress"]["journal"])


def main():
    # with open('test_cases/JournalPublished.txt', 'r') as file:
        # for line in file.readlines():
            # print(line.strip())
            # print(b.get_category())
            # print("Authors: ", end="")
            # for item in b.get_authors():
            #     print(item, end="  ")
            # print("\nYear: " + b.get_year())
            # print("Title: " + b.get_title())
            # print("Journal: " + b.get_journal())
            # print("Volume Number: " + b.get_volume())
            # print("Issue Number: " + b.get_issue())
            # print("Page Number: " + b.get_start_page() + " to " + b.get_end_page())
            # print()
            # if b.get_category() == Defs.JournalInPress:
            #     print(b.get_original().strip())
            #     print(b.get_category())
            #     print("Authors: ", end="")
            #     for item in b.get_authors():
            #         print(item, end="  ")
            #     print("\nYear: " + b.get_year())
            #     print("Title: " + b.get_title())
            #     print("Journal: " + b.get_journal())
            #     print()
    text = "Becker, T. E., Atinc, G., Breaugh, J. A., Carlson, K. D., Edwards, J. R., & Spector, P. E. (2016). " \
           "Statistical control in correlational studies: 10 essential recommendations for organizational researchers. " \
           "Journal of Organizational Behavior, 37, 157–167."
    ref = JournalPublished(text)
    print(ref.encode(CodeBook.AMJ))
    text1 = "Becker, T. E., Atinc, G., Breaugh, J. A., Carlson, K. D., Edwards, J. R., & Spector, P. E. (in press). " \
            "Statistical control in correlational studies: 10 essential recommendations for organizational researchers. " \
            "Journal of Organizational Behavior."
    ref1 = JournalInPress(text1)
    print(ref1.encode(CodeBook.AMJ))


if __name__ == "__main__":
    main()
