from Book import *
from Chapter import *
from Journal import *
from Others import *
import Transfer
import re
import utils
import operator


def decode(original):
    """
    classifier
    :param original: original text
    :return: a Reference Object
    """

    # Others
    if re.search("[Rr]etrieved\sfrom", original):
        try:
            info = utils.get_body(original)
        except AttributeError:
            return Other(original)
        re.sub("ed\.", "ed", info)
        k = info.count(".") + info.count("?") + info.count("!")
        if k <= 1:
            return Website(original)
        else:
            return OnLineJournal(original)

    # Chapter
    if re.search("In.*\([Ee]ds*\.*\)", original):
        if "(in press)" in original:
            return ChapterInPress(original)
        else:
            return ChapterPublished(original)

    # JournalPublished or BookPublished
    body = utils.get_body(original)
    if not body:
        return Other(original)

    if "(in press)" not in original:
        if re.search("\d+(?:\(\d+\))*,", body):
            return JournalPublished(original)
        else:
            return BookPublished(original)

    # JournalInPress or BookInPress
    body = re.sub("ed\.", "ed", body)
    k = body.count(".") + body.count("?") + body.count("?")
    if k <= 1:
        return BookInPress(original)
    else:
        return JournalInPress(original)


def encode_old(reference, journal):
    """
    encode reference object to a specific journal
    :param reference: a Reference Object
    :param journal: any journal in Defs
    :return: formatted string
    """
    return Transfer.encode(reference, journal)


def encode(reference, journal):
    if journal == Defs.AMJ:
        return reference.encode(CodeBook.AMJ)
    elif journal == Defs.AMR:
        return reference.encode(CodeBook.AMJ)
    elif journal == Defs.HR:
        return reference.encode(CodeBook.HR)
    elif journal == Defs.ASQ:
        return reference.encode(CodeBook.ASQ)


def compare(original, journal):
    old = encode_old(decode(original), journal)
    new = encode(decode(original), journal)
    if not operator.eq(old.strip(), new.strip()):
        print(old)
        print(new)
        print()


def test(original, journal):
    return encode(decode(original), journal)


def transfer(input_text, journal):
    """
    split input and transfer format
    :param input_text: original text get from website
    :param journal: journal chosen in website
    :return: a list of {"text": formatted string, "tag": True if transferred, False otherwise}
    """
    references = input_text.split("\n")
    output = []
    for item in references:
        if item == "":
            continue
        ref = decode(item)
        if not ref:
            output.append({"text": "Error. Please check your format.", "tag": False})
        else:
            output.append({"text": encode(ref, journal), "tag": ref.is_parsed()})
    return output


def main():
    with open("test_cases/others.txt") as file:
        for line in file.readlines():
            # print(line.strip())
            # print(encode2(decode(line), "ASQ"))
            # print()
            print(test(line, "ASQ"))
            print()


if __name__ == "__main__":
    main()