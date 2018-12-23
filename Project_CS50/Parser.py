from Book import BookPublished, BookInPress, BookOnline
from Chapter import ChapterPublished, ChapterInPress, ChapterOnline
from Journal import JournalPublished, JournalInPress, JournalOnLine
from Classifier import Classifier
import Transfer

def decode(original):
    # classify
    category = Classifier(original).classify()

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
    print(len(reference.getAuthors()))
    return Transfer.decode(reference, journal)


def transfer(input, journal):
    references = input.split("\n")
    # for item in references:
    #     print(item)
    #     print(Classifier(item).classify())
    output = []
    for item in references:
        if item == "":
            continue
        ref = decode(item)
        if not ref:
            output.append({"tag": False, "text": "Error. Please check your format."})
        else:
            # print(code(ref, journal))
            output.append({"tag": ref.isParsed(), "text": code(ref, journal)})
    return output


