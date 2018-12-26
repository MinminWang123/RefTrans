from Book import BookPublished, BookInPress, BookOnline
from Chapter import ChapterPublished, ChapterInPress, ChapterOnline
from Journal import JournalPublished, JournalInPress, JournalOnLine
from Classifier import Classifier
import Transfer
import Defs

def decode(original):
    # classify
    category = Classifier(original).classify()

    # instantiation
    if category == Defs.BookPublished:
        item = BookPublished(original)
    elif category == Defs.BookInPress:
        item = BookInPress(original)
    elif category == Defs.BookOnLine:
        item = BookOnline(original)
    elif category == Defs.ChapterPublished:
        item = ChapterPublished(original)
    elif category == Defs.ChapterInPress:
        item = ChapterInPress(original)
    elif category == Defs.ChapterOnLine:
        item = ChapterOnline(original)
    elif category == Defs.JournalPublished:
        item = JournalPublished(original)
    elif category == Defs.JournalInPress:
        item = JournalInPress(original)
    elif category == Defs.JournalOnLine:
        item = JournalOnLine(original)
    else:
        item = None

    return item


def encode(reference, journal):
    return Transfer.encode(reference, journal)


def transfer(input, journal):
    references = input.split("\n")
    output = []
    for item in references:
        if item == "":
            continue
        ref = decode(item)
        if not ref:
            output.append({"tag": False, "text": "Error. Please check your format."})
        else:
            print(ref.isParsed())
            output.append({"text": encode(ref, journal), "tag": ref.isParsed()})
    return output


