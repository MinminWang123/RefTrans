import re


class Classifier(object):
    def __init__(self, original):
        self._original = original

    def classify(self):
        if re.search("In.*\([Ee]ds*\.*\)", self._original):
            if "(in press)" in self._original:
                category = "ChapterInPress"
            elif "Retrieved from" in self._original:
                category = "ChapterOnLine"
            else:
                category = "ChapterPublished"
            return category
        if "http" in self._original:
            info = re.search(".*?\)\..*?[\.\?]\s(.*?)http", self._original).group(1)
        else:
            info = re.search(".*?\)\..*?[\.\?]\s(.*)", self._original).group(1)
        if re.search("\d", info):
            if "(in press)" in self._original:
                category = "JournalInPress"
            elif "Retrieved from" in self._original:
                category = "JournalOnLine"
            else:
                category = "JournalPublished"
        else:
            if "(in press)" in self._original:
                category = "BookInPress"
            elif "Retrieved from" in self._original:
                category = "BookOnLine"
            else:
                category = "BookPublished"
        return category


def main():
    with open("temp.txt", "r") as file:
        for line in file.readlines():
            print(Classifier(line).classify())


if __name__ == "__main__":
    main()