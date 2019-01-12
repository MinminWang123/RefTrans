"""
File: Others.py
Define OnLineJournal, Website, Other
"""


from Reference import Reference
import utils
import Defs
from Handler import *


"""
class OnLineJournal
standard format: author(s) (year). title. journal. Retrieved from source
initialize:   OnLineJournal(str original)
get_category: return Defs.OnLineJournal
get_original: return str original
is_parsed:    return True if successfully parsed, False if any field fails
get_authors:  return a list of Author / str "error in author(s)"
get_year:     return str year / "error in year"
get_title:    return str title("." excluded, "?" & "!" included) / "error in title"
get_journal:  return str journal / "error in journal"
get_source:   return str source if present, "" otherwise

encode_authors(): return Handler.authors
encode_year():    return Handler.general
encode_title():   return Handler.title
encode_journal(): return Handler.general
encode_source():  return Handler.general
encode()
"""


class OnLineJournal(Reference):

    def __init__(self, original):
        Reference.__init__(self, original)
        self._category = Defs.OnLineJournal

    def get_category(self):
        return self._category

    def _parse_title(self):
        self._parse_journal()
        if self.get_journal() == "error in journal":
            exp = r"^(.*[\.\?\!])\s"
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

    def encode_title(self, dic):
        return Handler.title(self.get_title(), dic)

    def _parse_journal(self):
        exp = re.sub(r"\?", '.', self._get_body())
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
               + self.encode_title(codebook["OnLineJournal"]["title"]) \
               + self.encode_journal(codebook["OnLineJournal"]["journal"]) \
               + self.encode_source(codebook["source"])

"""
class Website
standard format: author(s) (year). title. Retrieved from source
initialize:   Website(str original)
get_category: return Defs.Website
get_original: return str original
is_parsed:    return True if successfully parsed, False if any field fails
get_authors:  return a list of Author / str "error in author(s)" / str original
get_year:     return str year / "error in year"
get_title:    return str title("." excluded, "?" & "!" included) / "error in title"
get_source:   return str source if present, "" otherwise

encode_authors(): return Handler.authors
encode_year():    return Handler.general
encode_title():   return Handler.title
encode_source():  return Handler.general
encode()
"""


class Website(Reference):
    # author, year, title, (Retrieved from) Source
    def __init__(self, original):
        Reference.__init__(self, original)
        self._category = Defs.Website

    def get_category(self):
        return self._category

    def _parse_author(self):
        try:
            self._authors = re.search(r"(.+?)\.*\s*\(", self._original).group(1).strip()
        except AttributeError:
            self._parsed = False
            self._authors = "error in author"

    def get_authors(self):
        if re.search(r"\w.*?,(?:\s*[A-Z]\.)*", re.search(r"(.*?)\(", self._original).group(1)):
            return Reference.get_authors(self)
        else:
            self._parse_author()
            return self._authors

    def _parse_title(self):
        try:
            self._title = re.search("^(.+)[Rr]etrieved", self._get_body()).group(1).strip()
            if len(self._title) == 0:
                self._parsed = False
                self._title = "error in title"
        except AttributeError:
            self._parsed = False
            return "error in title"

    def get_title(self):
        self._parse_title()
        return self._title.strip(".")

    def encode_title(self, dic):
        return Handler.title(self.get_title(), dic)

    def encode(self, codebook):
        return self.encode_authors(codebook["authors"]) + self.encode_year(codebook["year"]) \
               + self.encode_title(codebook["Website"]["title"]) \
               + self.encode_source(codebook["source"])


"""
class Other
Reference that cannot be categorized
initialize:   Other(str original)
is_parsed:    return False
get_category: return Defs.Other
get_original: return original

encode_original(): return Handler.general
encode()
"""


class Other(object):
    def __init__(self, original):
        self._original = original
        self._category = Defs.Other

    @staticmethod
    def is_parsed():
        return False

    def get_original(self):
        return self._original

    def get_category(self):
        return self._category

    def encode_original(self, dic):
        return Handler.general(self.get_original(), dic)

    def encode(self, codebook):
        return self.encode_original(codebook["Other"]["original"])


def main():
    # with open('test_cases/OnLineJournal.txt', 'r') as file:
    #     for line in file.readlines():
    #         b = OnLineJournal(line)
    #         print(line.strip())
    #         print(b.encode_authors())
    #         print(b.encode_year())
    #         print(b.encode_title())
    #         print(b.encode_journal())
    #         print(b.encode_source())
    #         print()
            # if b.get_category() == Defs.OnLineJournal:
            #     print(b.get_category())
            #     print("Authors: ", end="")
            #     for item in b.get_authors():
            #         print(item, end="  ")
            #     print("\nYear: " + b.get_year())
            #     print("Title: " + b.get_title())
            #     print("Journal: " + b.get_journal())
            #     print("Source: " + b.get_source())
            #     print()
            # if b.get_category() == Defs.Website:
            #     print(b.get_category())
            #     print("Authors: ", end="")
            #     for item in b.get_authors():
            #         print(item, end="  ")
            #     print("Year: " + b.get_year())
            #     print("Title: " + b.get_title())
            #     print("Source: " + b.get_source())
            #     print()
            # if b.get_category() == Defs.Other:
            #     print(b.get_original())
    text1 = "Ashkenas, R. (2012, September). More direct reports make life easier. Harvard Business Review. Retrieved from https://hbr.org/2012/09/moredirect-reports-make-life.html"
    text2 = "Fortune. (2017, August 8). Google’s gender problem is actually a tech problem. Retrieved from http://fortune.com/2017/08/08/google-genderstruggle-tech/"
    text3 = "Cycling Weekly. (2013). Retrieved June 1, 2016, from http://www.cyclingweekly.co.uk"

    print(OnLineJournal(text1).encode(CodeBook.AMJ))
    print(Website(text2).encode(CodeBook.AMJ))
    print(Other(text3).encode(CodeBook.AMJ))


if __name__ == "__main__":
    main()

