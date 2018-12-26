import re


class Author(object):
    _firstName = ""
    _lastName = ""

    def getLastName(self):
        return self._lastName

    def getFirstName(self):
        return self._firstName

    def toFormatString(self, f_cat=". ", fl_cat=", "):
        result = ""
        for item in self.getFirstName():
            result += item + f_cat
        return self.getLastName() + fl_cat + result.strip()

    def toReverseFormatString(self, f_cat=". ", fl_cat=""):
        result = ""
        for item in self.getFirstName():
            result += item + f_cat
        return result + fl_cat + self.getLastName()

    def __str__(self):
        result = ""
        for item in self.getFirstName():
            result += item + ". "
        return self.getLastName() + ", " + result.strip()


class AuthorLF(Author):
    def __init__(self, original):
        self._original = original
        self._lastName = self._original.split(',')[0]
        self._firstName = re.findall('[A-Z]', self._original.split(',')[1])


class AuthorFL(Author):
    def __init__(self, original):
        self._original = original
        self._lastName = self._original.split('.')[-1].strip()
        self._firstName = []
        for letter in re.findall('[A-Z]\.', self._original):
            self._firstName.append(letter.strip('.'))
