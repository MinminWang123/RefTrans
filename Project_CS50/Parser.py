from Book import BookPublished, BookInPress, BookOnline
from Chapter import ChapterPublished, ChapterInPress, ChapterOnline
from Journal import JournalPublished, JournalInPress, JournalOnLine
from Classifier import Classifier


def decode(original):
    # classify
    category = Classifier.classify(original)

    # instantiation
    if category == "BookPublished":
        item = BookPublished(original)
    elif category == "BookInPress":
        item = BookInPress(original)
    elif category == "BookOnline":
        item = BookOnline(original)
    elif category == "ChapterPublished":
        item = ChapterPublished(original)
    elif category == "ChapterInPress":
        item = ChapterInPress(original)
    elif category == "ChapterOnLine":
        item = ChapterOnline(original)
    elif category == "JournalPublished":
        item = JournalPublished(original)
    elif category == "JournalInPress":
        item = JournalInPress(original)
    elif category == "JournalOnLine":
        item = JournalOnLine(original)
    else:
        item = None

    return item


def code(reference, journal):
    pass


def transfer(original, journal):
    return code(decode(original), journal)

