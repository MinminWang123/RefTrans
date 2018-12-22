import re


class Author(object):
    pass


class AuthorLF(Author):
    def __init__(self, original):
        self._original = original
        self._lastName = self._original.split(',')[0]
        self._firstName = re.findall('[A-Z]', self._original.split(',')[1])

    def getLastName(self):
        return self._lastName

    def getFirstName(self):
        return self._firstName

    def __str__(self):
        return self.getLastName() + ", " + " ".join(self.getFirstName())


class AuthorFL(Author):
    def __init__(self, original):
        self._original = original
        self._lastName = self._original.split('.')[-1].strip()
        self._firstName = []
        for letter in re.findall('[A-Z]\.', self._original):
            self._firstName.append(letter.strip('.'))

    def getLastName(self):
        return self._lastName

    def getFirstName(self):
        return self._firstName

    def __str__(self):
        return self.getLastName() + ", " + " ".join(self.getFirstName())



