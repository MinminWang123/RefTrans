import re
import CodeBook
import utils

"""
File Handler.py
Define Handler
"""

"""
Handler.general: 
  head, tail, bold, italic, end
Handler.authors: 
  ln_end, char_end, char_int, fn_end, n_int, seq1, seq2, two_int, front_int, back_int, head, tail, bold, italic, end
Handler.editors:
  ln_end, char_end, char_int, fn_end, n_int, seq1, seq2, two_int, front_int, back_int, head, tail, bold, italic, end, ed1, ed2
Handler.issue:
  head, tail, bold, italic, end, required
Handler.pages:
  page_int, head, tail, bold, italic, end
Handler.page_addition:
  head, tail, bold, italic, end
Handler.title:
  ed_pattern, head, tail, bold, italic, inner_end, end
"""


class Handler(object):

    @staticmethod
    def bold(text):
        return "<b>" + text + "</b>"

    @staticmethod
    def italic(text):
        return "<i>" + text + "</i>"

    @staticmethod
    def _name(name, dic, seq="lf"):
        """
        handler of name
        :param name: Author object or str
        :param dic: a dictionary whose keys are ln_end, char_end, char_int, fn_end, n_int
        ln_end: end of last name
        char_end: end of character of first name
        char_int: interval of characters
        fn_end: end of first name
        n_int: interval of the two names
        :param seq: "lf" for last name + first name, "fl" for first name + last name
        :return str name
        """
        if type(name) == str:
            return name
        fn = ""
        if len(name.get_first_name()) > 0:
            for char in name.get_first_name()[:-1]:
                fn += char + dic["char_end"] + dic["char_int"]
            fn += name.get_first_name()[-1] + dic["char_end"] + dic["fn_end"]
            fn = re.sub(r"\s-", "-", fn)
        if seq == "lf":
            name = name.get_last_name() + dic["ln_end"] + dic["n_int"] + fn
        elif seq == "fl":
            name = fn + dic["n_int"] + name.get_last_name()
        else:
            name = name
        return name

    @classmethod
    def _name_list(cls, names, dic):
        """
        handler of a list of names
        :param names: a list of Author object or str
        :param dic: a dictionary whose keys are
        ln_end, char_end, char_int, fn_end, n_int, seq1, seq2, two_int, front_int, back_int
        ln_end - n_int: same as _name()
        seq1: seq for the first author
        seq2: seq for other authors
        two_int: interval for two authors
        front_int: interval for front authors when there're more than two authors
        back_int: interval for last tow authors when there're more than two authors
        :return: str
        """
        if type(names) == str:
            return names

        # single author
        if len(names) == 1:
            string = cls._name(names[0], dic, seq=dic["seq1"])

        # two authors
        elif len(names) == 2:
            string = cls._name(names[0], dic, seq=dic["seq1"]) + dic["two_int"] + cls._name(names[1], dic, seq=dic["seq2"])

        # more than two authors
        else:
            string = cls._name(names[0], dic, seq=dic["seq1"]) + dic["front_int"]
            for author in names[1:-2]:
                string += cls._name(author, dic, seq=dic["seq2"]) + dic["front_int"]
            string += cls._name(names[-2], dic, seq=dic["seq2"]) + dic["back_int"] + cls._name(names[-1], dic, seq=dic["seq2"])

        return string

    @classmethod
    def general(cls, original, dic):
        """
        handler of general types
        :param original: str
        :param dic: a dictionary whose keys are head, tail, bold, italic, end
        head: head modifier
        tail: tail modifier
        bold: True if bold, False otherwise
        italic: True if italic, False otherwise
        end: end
        :return: str
        """

        # bold or italic
        string = original
        if dic["bold"]:
            string = cls.bold(string)
        if dic["italic"]:
            string = cls.italic(string)

        return dic["head"] + string + dic["tail"] + dic["end"]

    @classmethod
    def authors(cls, authors, dic):
        """
        handler for authors
        :param authors: a list of Author object or str
        :param dic: a dictionary whose keys are
        ln_end, char_end, char_int, fn_end, n_int, seq1, seq2, two_int, front_int, back_int, head, tail, bold, italic, end
        ln_end - n_int: same as cls._name()
        seq1 - back_int: same as cls._name_list()
        head - end: same as cls.general()
        :return: str
        """
        if type(authors) == str:
            string = authors
        else:
            string = cls._name_list(authors, dic)

        return cls.general(string, dic)

    @classmethod
    def editors(cls, editors, dic):
        """
        handler of editors
        :param editors: a list of Author object or str
        :param dic: a dictionary whose keys are
        ln_end, char_end, char_int, fn_end, n_int, seq1, seq2, two_int, front_int, back_int,
        head, tail, bold, italic, end, ed1, ed2
        ln_end - back_int: same as cls._name_list()
        head - end: same as cls.general()
        ed1: note if there's only one editor
        ed2: note if there're more than one editor
        :return: str
        """
        if type(editors) == str:
            string = editors

        # single editor
        elif len(editors) == 1:
            string = cls._name_list(editors, dic) + dic["ed1"]

        # multiple editors
        else:
            string = cls._name_list(editors, dic) + dic["ed2"]

        return cls.general(string, dic)

    @classmethod
    def issue(cls, issue, dic):
        """
        handler of issue number
        :param issue: str
        :param dic: a dictionary whose keys are head, tail, bold, italic, end, required
        required: True if issue number is necessary, False otherwise
        omitted: True if issue number is omitted, False otherwise
        :return: str
        """
        if dic["required"]:
            return cls.general(issue, dic)
        if dic["omitted"]:
            return dic["end"]
        if issue:
            return cls.general(issue, dic)
        else:
            return dic["end"]

    @classmethod
    def pages(cls, start_page, end_page, dic):
        """
        handler of pages
        :param start_page: str
        :param end_page: str
        :param dic: a dictionary whose keys are page_int, head, tail, bold, italic, end
        page_int: interval between pages
        shrink: True if end page shrinks, False otherwise
        :return: str
        """
        if dic["shrink"]:
            end_page = utils.shrink_page(start_page, end_page)
        string = start_page + dic["page_int"] + end_page
        return cls.general(string, dic)

    @classmethod
    def page_addition(cls, page_addition, dic):
        """
        handler of page_addition
        :param page_addition: str
        :param dic: a dictionary whose keys are head, tail, bold, italic, end
        :return: str
        """
        if page_addition:
            return cls.general(page_addition, dic)
        else:
            return dic["end"]

    @classmethod
    def title(cls, title, dic):
        """
        handler of title
        :param title: str
        :param dic: a dictionary whose keys are ed_pattern, head, tail, bold, italic, inner_end, end
        ed_pattern: 1: (xx ed.), 2: xx edn
        inner_end: end inside head and tail
        end: end outside of head and tail
        :return: str
        """
        # split text if (xxxed.) appears
        if re.search(r'\(.*ed\.\)', title):
            string = re.search(r"(.*)(\(.*ed\.?\))", title).group(1).strip()
            ed = re.search(r"(.*)\((.*ed\.?)\)", title).group(2).strip()
        else:
            string = title
            ed = ""

        # edit eds.
        # pattern 1: (xx ed.)
        # pattern 2: xx edn
        if ed:
            if dic["ed_pattern"] == 1:
                ed = " (" + ed + ")"
            elif dic["ed_pattern"] == 2:
                ed = ", " + re.sub(r"ed\.?", "edn", ed)

        # bold or italic
        if dic["bold"]:
            string = cls.bold(string)
        if dic["italic"]:
            string = cls.italic(string)

        # if there's an inner_end or tail
        if dic["inner_end"] or dic["tail"]:

            # if ? or ! at the end of title, do not add inner_end
            if re.search(r".*[?!]$", title):
                string = dic["head"] + string + ed + dic["inner_end"].strip(".") + dic["tail"] + dic["end"]
            # if ? or ! not at the end of title, add inner_end
            else:
                string = dic["head"] + string + ed + dic["inner_end"] + dic["tail"] + dic["end"]

        # if there isn't an inner end nor tail
        else:
            if re.search(r".*[?!]$", title):
                string = dic["head"] + string + ed + dic["tail"] + dic["end"].strip(".")
            else:
                string = dic["head"] + string + ed + dic["tail"] + dic["end"]

        return string


def main():
    print(Handler.general("1992", CodeBook.AMJ["year"]))
    print(Handler.authors("American Psychological Associate.", CodeBook.AMJ["authors"]))


if __name__ == "__main__":
    main()
