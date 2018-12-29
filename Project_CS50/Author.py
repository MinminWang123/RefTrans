import re


class Author(object):
    _first_name = ""
    _last_name = ""

    def get_last_name(self):
        return self._last_name

    def get_first_name(self):
        return self._first_name

    def to_format_string(self, f_cat=". ", fl_cat=", "):
        result = ""
        for item in self.get_first_name():
            result += item + f_cat
        return self.get_last_name() + fl_cat + result.strip()

    def to_reverse_format_string(self, f_cat=". ", fl_cat=""):
        result = ""
        for item in self.get_first_name():
            result += item + f_cat
        return result + fl_cat + self.get_last_name()

    def __str__(self):
        result = ""
        for item in self.get_first_name():
            result += item + ". "
        return self.get_last_name() + ", " + result.strip()


class AuthorLF(Author):
    def __init__(self, original):
        self._original = original
        self._last_name = self._original.split(',')[0]
        self._first_name = re.findall('[A-Z]', self._original.split(',')[1])


class AuthorFL(Author):
    def __init__(self, original):
        self._original = original
        self._last_name = self._original.split('.')[-1].strip()
        self._first_name = []
        for letter in re.findall('[A-Z]\.', self._original):
            self._first_name.append(letter.strip('.'))
