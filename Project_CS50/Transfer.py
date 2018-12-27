import Defs
import re


def encode(reference, journal):
    if journal == Defs.AMJ or journal == Defs.AMR:
        return parse2AMJ(reference)
    if journal == Defs.HR:
        return parse2HR(reference)


def parse2AMJ(reference):
    if reference.getCategory() == Defs.BookPublished:
        return book_published_AMJ(reference)
    elif reference.getCategory() == Defs.ChapterPublished:
        return chapter_published_AMJ(reference)
    elif reference.getCategory() == Defs.JournalPublished:
        return journal_published_AMJ(reference)
    elif reference.getCategory() == Defs.BookInPress:
        return book_inpress_AMJ(reference)
    elif reference.getCategory() == Defs.ChapterInPress:
        return chapter_inpress_AMJ(reference)
    elif reference.getCategory() == Defs.JournalInPress:
        return journal_inpress_AMJ(reference)


def parse2HR(reference):
    if reference.getCategory() == Defs.BookPublished:
        return book_published_HR(reference)
    elif reference.getCategory() == Defs.ChapterPublished:
        return chapter_published_HR(reference)
    elif reference.getCategory() == Defs.JournalPublished:
        return journal_published_HR(reference)
    elif reference.getCategory() == Defs.BookInPress:
        return book_inpress_HR(reference)
    elif reference.getCategory() == Defs.ChapterInPress:
        return chapter_inpress_HR(reference)
    elif reference.getCategory() == Defs.JournalInPress:
        return journal_inpress_HR(reference)


def book_published_AMJ(book):
    author_str = getAuthorStr(book.getAuthors())
    title_str = book_title_filter(book.getTitle())
    return "{0} {1}. {2}. {3}{4}: {5}.".format(author_str, book.getYear(), title_str,
                                               book.getCity(),
                                               ", " + book.getState() if book.getState() else "",
                                               book.getPublisher())


def chapter_published_AMJ(chapter):
    author_str = getAuthorStr(chapter.getAuthors())
    editor_str = getReverseEditorStr(chapter.getEditors())
    return "{0} {1}. {2}. In {3}, <i><b>{4}</b></i>{5}: {6}. {7}{8}: {9}.".format(author_str,
                                                                                  chapter.getYear(),
                                                                                  chapter.getChapterTitle(),
                                                                                  editor_str,
                                                                                  chapter.getBookTitle(),
                                                                                  ", " + chapter.getPageAddition() if chapter.getPageAddition() else "",
                                                                                  chapter.getStartPage() + "-" + chapter.getEndPage(),
                                                                                  chapter.getCity(),
                                                                                  ", " + chapter.getState() if chapter.getState() else "",
                                                                                  chapter.getPublisher())


def journal_published_AMJ(journal):
    author_str = getAuthorStr(journal.getAuthors())
    return "{0} {1}. {2}. <i><b>{3}</b></i>, {4}{5}: {6}.".format(author_str, journal.getYear(), journal.getTitle(),
                                                                  journal.getJournal(),
                                                                  journal.getVolume(),
                                                                  "(" + journal.getIssue() + ")" if journal.getIssue() else "",
                                                                  journal.getStartPage() + "-" + journal.getEndPage())


def book_inpress_AMJ(book):
    author_str = getAuthorStr(book.getAuthors())
    title_str = book_title_filter(book.getTitle())
    return "{0} {1}. {2}.".format(author_str, book.getYear(), title_str)


def chapter_inpress_AMJ(chapter):
    author_str = getAuthorStr(chapter.getAuthors())
    editor_str = getReverseEditorStr(chapter.getEditors())
    return "{0} {1}. {2}. In {3}, <i><b>{4}</b></i>.".format(author_str,
                                                             chapter.getYear(),
                                                             chapter.getChapterTitle(),
                                                             editor_str,
                                                             chapter.getBookTitle())


def journal_inpress_AMJ(journal):
    author_str = getAuthorStr(journal.getAuthors())
    return "{0} {1}. {2}. <i><b>{3}</b></i>.".format(author_str, journal.getYear(), journal.getTitle(),
                                                     journal.getJournal())


def online_resources_AMJ(journal):
    author_str = getAuthorStr(journal.getAuthors())
    journal_str = (("<i><b>" + journal.getJournal() + "</b></i>. ") if journal.getJournal() else "")
    return "{0} {1}. {2}. {3}Retrieved from {4}".format(author_str, journal.getYear(),
                                                        journal.getTitle(),
                                                        journal_str,
                                                        journal.getSource())


def other_AMJ(journal):
    return journal.getOriginal()


def getAuthorStr(authors, cat1=", ", cat2=", & ", f_cat=". ", fl_cat=", "):
    author_str = authors[0].toFormatString(f_cat=f_cat, fl_cat=fl_cat)
    for author in authors[1:-1]:
        author_str += cat1 + author.toFormatString(f_cat=f_cat, fl_cat=fl_cat)
    if (len(authors)) > 1:
        author_str += cat2 + authors[-1].toFormatString(f_cat=f_cat, fl_cat=fl_cat)
    return author_str


def getEditorStr(editors, cat1=", ", cat2=" & ", eds=" (Eds.)", ed=" (Ed.)", f_cat=". ", fl_cat=", "):
    editor_str = editors[0].toFormatString(f_cat=f_cat, fl_cat=fl_cat)
    for editor in editors[1:-1]:
        editor_str += cat1 + editor.toFormatString(f_cat=f_cat, fl_cat=fl_cat)
    if (len(editors)) > 1:
        editor_str += cat2 + editors[-1].toFormatString(f_cat=f_cat, fl_cat=fl_cat) + eds
    else:
        editor_str += ed
    return editor_str


def getReverseEditorStr(editors, cat1=", ", cat2=" & ", eds=" (Eds.)", ed=" (Ed.)", f_cat=". ", fl_cat=", "):
    editor_str = editors[0].toReverseFormatString(f_cat=f_cat, fl_cat=fl_cat)
    for editor in editors[1:-1]:
        editor_str += cat1 + editor.toReverseFormatString(f_cat=f_cat, fl_cat=fl_cat)
    if (len(editors)) > 1:
        editor_str += cat2 + editors[-1].toReverseFormatString(f_cat=f_cat, fl_cat=fl_cat) + eds
    else:
        editor_str += ed
    return editor_str


def book_title_filter(title, bold=True, italic=True):
    title_sub = ""
    new_title = title
    if re.search('\(.*?ed\.\)', title):
        new_title = re.search('(.*?)(\(.*?ed\.\))', title).group(1).strip()
        title_sub = " " + re.search('(.*?)(\(.*?ed\.\))', title).group(2).strip()
    if bold:
        new_title = "<b>" + new_title + "</b>"
    if italic:
        new_title = "<i>" + new_title + "</i>"
    return new_title + title_sub


def book_published_HR(book):
    author_str = getAuthorStr(book.getAuthors(), cat1=", ", cat2=" and ", f_cat="", fl_cat=" ")
    title_str = book_title_filter(book.getTitle(), bold=False, italic=True)
    return "{0} ({1}) {2}. {3}{4}: {5}.".format(author_str, book.getYear(), title_str,
                                                book.getCity(),
                                                ", " + book.getState() if book.getState() else "",
                                                book.getPublisher())


def chapter_published_HR(chapter):
    author_str = getAuthorStr(chapter.getAuthors(), cat1=", ", cat2=" and ", f_cat="", fl_cat=" ")
    editor_str = getEditorStr(chapter.getEditors(), ed=" (ed.)", eds=" (eds)", cat1=", ", cat2=", ", f_cat="",
                              fl_cat=" ")
    return "{0} ({1}) {2}. In: {3} <i>{4}</i>. {5}{6}: {7}{8}, {9}.".format(author_str,
                                                                            chapter.getYear(),
                                                                            chapter.getChapterTitle(),
                                                                            editor_str,
                                                                            chapter.getBookTitle(),
                                                                            chapter.getCity(),
                                                                            ", " + chapter.getState() if chapter.getState() else "",
                                                                            chapter.getPublisher(),
                                                                            ", " + chapter.getPageAddition() if chapter.getPageAddition() else "",
                                                                            chapter.getStartPage() + "-" + chapter.getEndPage()
                                                                            )


def journal_published_HR(journal):
    author_str = getAuthorStr(journal.getAuthors(), cat1=", ", cat2=" and ", f_cat="", fl_cat=" ")
    return "{0} ({1}) {2}. <i>{3}</i> {4}{5}: {6}.".format(author_str, journal.getYear(), journal.getTitle(),
                                                           journal.getJournal(),
                                                           journal.getVolume(),
                                                           "(" + journal.getIssue() + ")" if journal.getIssue() else "",
                                                           journal.getStartPage() + "-" + journal.getEndPage())


def book_inpress_HR(book):
    author_str = getAuthorStr(book.getAuthors(), cat1=", ", cat2=" and ", f_cat="", fl_cat=" ")
    title_str = book_title_filter(book.getTitle(), bold=False, italic=True)
    return "{0} ({1}) {2}.".format(author_str, book.getYear(), title_str)


def chapter_inpress_HR(chapter):
    author_str = getAuthorStr(chapter.getAuthors(), cat1=", ", cat2=" and ", f_cat="", fl_cat=" ")
    editor_str = getEditorStr(chapter.getEditors(), ed=" (ed.)", eds=" (eds)", cat1=", ", cat2=", ", f_cat="",
                              fl_cat=" ")
    return "{0} ({1}) {2}. In: {3} <i>{4}</i>.".format(author_str,
                                                       chapter.getYear(),
                                                       chapter.getChapterTitle(),
                                                       editor_str,
                                                       chapter.getBookTitle()
                                                       )


def journal_inpress_HR(journal):
    author_str = getAuthorStr(journal.getAuthors(), cat1=", ", cat2=" and ", f_cat="", fl_cat=" ")
    return "{0} ({1}) {2}. <i>{3}</i>.".format(author_str, journal.getYear(), journal.getTitle(),
                                               journal.getJournal())


def online_resources_HR(journal):
    author_str = getAuthorStr(journal.getAuthors())
    journal_str = (("<i>" + journal.getJournal() + "</i>. ") if journal.getJournal() else "")
    return "{0} ({1}) {2}. {3}Available at: {4}".format(author_str, journal.getYear(),
                                                        journal.getTitle(),
                                                        journal_str,
                                                        journal.getSource())


from Book import *
from Chapter import *
from Journal import *


def main():
    c_input = "Chen, G., Mathieu, J. E., & Bliese, P. D. (2004). A framework for conducting multilevel construct validation. In F. J. Yammarino & F. Dansereau (Eds.), Research in multilevel issues: Multilevel issues in organizational behavior and processes (Vol. 3, pp. 273-303). Oxford, UK: Elsevier. http://dx.doi.org/10.1016/S1475-9144(04)03013-9"
    b_input = "Aiken, L. S., & West, S. G. (1991). Multiple regression: Testing and interpreting interactions. Newbury Park, CA: Sage."
    j_input = "Avey, J. B., Wernsing, T. S., & Palanski, M. E. (2012). Exploring the process of ethical leadership: The mediating role of employee voice and psychological ownership. Journal of Business Ethics, 107, 21–34. http://dx.doi.org/10.1007/s10551-012-1298-2"

    c = ChapterPublished(c_input)
    b = BookPublished(b_input)
    j = JournalPublished(j_input)

    c = ChapterInPress(c_input)
    b = BookInPress(b_input)
    j = JournalInPress(j_input)

    journal_type = "AMR"
    print("****")
    print("chapter:")
    print(encode(c, journal_type))
    print()
    print("book:")
    print(encode(b, journal_type))
    print()
    print("journal:")
    print(encode(j, journal_type))


if __name__ == "__main__":
    main()
