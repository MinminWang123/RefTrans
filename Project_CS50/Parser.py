from Book import *
from Chapter import *
from Journal import *
from Others import *
import Transfer
import re
import utils


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


def encode(reference, journal):
    """
    encode reference object to a specific journal
    :param reference: a Reference Object
    :param journal: any journal in Defs
    :return: formatted string
    """
    return Transfer.encode(reference, journal)


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
    string = "Singleton, R. A., & Straits, B. C. (2010). Approaches to social research (5th ed.). New York, NY: Oxford University Press."
    print(decode(string).get_category())
    print(decode(string).get_title())
    print(encode(decode(string), Defs.AMJ))



if __name__ == "__main__":
    main()