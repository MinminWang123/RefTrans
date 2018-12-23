import Defs


def decode(reference, journal):
    if journal == Defs.AMJ:
        return parse2AMJ(reference)


def parse2AMJ(reference):
    if reference.getCategory() == Defs.BookPublished:
        return BookPublished2AMJ(reference)
    elif reference.getCategory() == Defs.ChapterPublished:
        return ChapterPublished2AMJ(reference)
    elif reference.getCategory() == Defs.JournalPublished:
        return JournalPublished2AMJ(reference)


def BookPublished2AMJ(book):
    authors = book.getAuthors()
    author_str = authors[0].toString()
    for author in authors[1:-1]:
        author_str += ", " + author.toString()
    if (len(authors)) > 1:
        author_str += ", & " + authors[-1].toString()
    return "{0} {1}. <i><b>{2}</b></i>. {3}, {4}: {5}.".format(author_str, book.getYear(), book.getTitle(),
                                                               book.getCity(), book.getState(),
                                                               book.getPublisher())


def ChapterPublished2AMJ(chapter):
    authors = chapter.getAuthors()
    author_str = authors[0].toString()
    for author in authors[1:-1]:
        author_str += ", " + author.toString()
    if (len(authors)) > 1:
        author_str += ", & " + authors[-1].toString()

    editors = chapter.getEditors()
    editor_str = editors[0].toReverseString()
    for editor in editors[1:-1]:
        editor_str += ", " + editor.toReverseString()
    if (len(editors)) > 1:
        editor_str += " & " + editors[-1].toReverseString()
        return "{0} {1}. {2}. In {3} (Eds.), <i><b>{4}</b></i>: {5}. {6}, {7}: {8}.".format(author_str,
                                                                                            chapter.getYear(),
                                                                                            chapter.getChapterTitle(),
                                                                                            editor_str,
                                                                                            chapter.getBookTitle() + (
                                                                                                "" if chapter.getPageAddition() else chapter.getPageAddition()),
                                                                                            chapter.getStartPage() + "-" + chapter.getEndPage(),
                                                                                            chapter.getCity(),
                                                                                            chapter.getState(),
                                                                                            chapter.getPublisher())
    else:
        return "{0} {1}. {2}. In {3} (Ed.), <i><b>{4}</b></i>: {5}. {6}, {7}: {8}.".format(author_str,
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
    authors = journal.getAuthors()
    author_str = authors[0].toString()
    for author in authors[1:-1]:
        author_str += ", " + author.toString()
    if (len(authors)) > 1:
        author_str += ", & " + authors[-1].toString()
    return "{0} {1}. {2}. <i><b>{3}</b></i>, {4}: {5}.".format(author_str, journal.getYear(), journal.getTitle(),
                                                               journal.getJournal(),
                                                               journal.getVolume(),
                                                               journal.getStartPage() + "-" + journal.getEndPage())
