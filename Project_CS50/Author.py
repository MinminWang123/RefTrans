import re

class Author(object):
    _firstName = ""
    _lastName = ""

    def getLastName(self):
        return self._lastName

    def getFirstName(self):
        return self._firstName

    def toOnlySpaceString(self):
        result = ""
        for item in self.getFirstName():
            result += item
        return self.getLastName() + " " + result

    def toString(self):
        return self.__str__()

    def toReverseString(self):
        result = ""
        for item in self.getFirstName():
            result += item + ". "
        return result + self.getLastName()

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


