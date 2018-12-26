import Defs


def encode(reference, journal):
    if journal == Defs.AMJ:
        return parse2AMJ(reference)


def parse2AMJ(reference):
    if reference.getCategory() == Defs.BookPublished:
        return BookPublished2AMJ(reference)
    elif reference.getCategory() == Defs.ChapterPublished:
        return ChapterPublished2AMJ(reference)
    elif reference.getCategory() == Defs.JournalPublished:
        return JournalPublished2AMJ(reference)


def parse2AMR(reference):
    if reference.getCategory() == Defs.BookPublished:
        return BookPublished2AMR(reference)
    elif reference.getCategory() == Defs.ChapterPublished:
        return ChapterPublished2AMR(reference)
    elif reference.getCategory() == Defs.JournalPublished:
        return JournalPublished2AMR(reference)


def BookPublished2AMR(book):
    author_str = getAuthorStr(book.getAuthors())
    return "{0} {1}. <i><b>{2}</b></i>. {3}{4}: {5}.".format(author_str, book.getYear(), book.getTitle(),
                                                             book.getCity(),
                                                             ", " + book.getState() if book.getState() else "",
                                                             book.getPublisher())


def ChapterPublished2AMR(chapter):
    author_str = getAuthorStr(chapter.getAuthors())
    editor_str = getEditorStr(chapter.getEditors())
    return "{0} {1}. {2}. In {3}, <i><b>{4}</b></i>: {5}. {6}{7}: {8}.".format(author_str,
                                                                               chapter.getYear(),
                                                                               chapter.getChapterTitle(),
                                                                               editor_str,
                                                                               chapter.getBookTitle() + (
                                                                                   "" if chapter.getPageAddition() else chapter.getPageAddition()),
                                                                               chapter.getStartPage() + "-" + chapter.getEndPage(),
                                                                               chapter.getCity(),
                                                                               ", " + chapter.getState() if chapter.getState() else "",
                                                                               chapter.getPublisher())


def JournalPublished2AMR(journal):
    author_str = getAuthorStr(journal.getAuthors())
    return "{0} {1}. {2}. <i><b>{3}</b></i>, {4}{5}: {6}.".format(author_str, journal.getYear(), journal.getTitle(),
                                                                  journal.getJournal(),
                                                                  journal.getVolume(),
                                                                  "(" + journal.getIssue() + ")" if journal.getIssue() else "",
                                                                  journal.getStartPage() + "-" + journal.getEndPage())


def BookPublished2AMJ(book):
    author_str = getAuthorStr(book.getAuthors())
    return "{0} {1}. <i><b>{2}</b></i>. {3}, {4}: {5}.".format(author_str, book.getYear(), book.getTitle(),
                                                               book.getCity(), book.getState(),
                                                               book.getPublisher())


def ChapterPublished2AMJ(chapter):
    author_str = getAuthorStr(chapter.getAuthors())
    editor_str = getEditorStr(chapter.getEditors())
    return "{0} {1}. {2}. In {3}, <i><b>{4}</b></i>: {5}. {6}, {7}: {8}.".format(author_str,
                                                                                 chapter.getYear(),
                                                                                 chapter.getChapterTitle(),
                                                                                 editor_str,
                                                                                 chapter.getBookTitle() + (
                                                                                     "" if chapter.getPageAddition() else chapter.getPageAddition()),
                                                                                 chapter.getStartPage() + "-" + chapter.getEndPage(),
                                                                                 chapter.getCity(),
                                                                                 chapter.getState(),
                                                                                 chapter.getPublisher())


def JournalPublished2AMJ(journal):
    author_str = getAuthorStr(journal.getAuthors())
    return "{0} {1}. {2}. <i><b>{3}</b></i>, {4}: {5}.".format(author_str, journal.getYear(), journal.getTitle(),
                                                               journal.getJournal(),
                                                               journal.getVolume(),
                                                               journal.getStartPage() + "-" + journal.getEndPage())


def getAuthorStr(authors, cat1=", ", cat2=", & "):
    author_str = authors[0].toString()
    for author in authors[1:-1]:
        author_str += cat1 + author.toString()
    if (len(authors)) > 1:
        author_str += cat2 + authors[-1].toString()
    return author_str


def getEditorStr(editors, cat1 = ", ", cat2 = " & ", eds = " (Eds.)", ed=" (Ed.)"):
    editor_str = editors[0].toReverseString()
    for editor in editors[1:-1]:
        editor_str += cat1 + editor.toReverseString()
    if (len(editors)) > 1:
        editor_str += cat2 + editors[-1].toReverseString() + eds
    else:
        editor_str += ed
    return editor_str
