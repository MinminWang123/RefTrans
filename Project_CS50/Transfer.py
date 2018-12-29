import Defs
import re


def encode(reference, journal):
    if journal == Defs.AMJ or journal == Defs.AMR:
        return parse_to_amj(reference)
    if journal == Defs.HR:
        return parse_to_hr(reference)


def parse_to_amj(reference):
    if reference.get_category() == Defs.BookPublished:
        return book_published_amj(reference)
    elif reference.get_category() == Defs.ChapterPublished:
        return chapter_published_amj(reference)
    elif reference.get_category() == Defs.JournalPublished:
        return journal_published_amj(reference)
    elif reference.get_category() == Defs.BookInPress:
        return book_inpress_amj(reference)
    elif reference.get_category() == Defs.ChapterInPress:
        return chapter_inpress_amj(reference)
    elif reference.get_category() == Defs.JournalInPress:
        return journal_inpress_amj(reference)


def parse_to_hr(reference):
    if reference.get_category() == Defs.BookPublished:
        return book_published_hr(reference)
    elif reference.get_category() == Defs.ChapterPublished:
        return chapter_published_hr(reference)
    elif reference.get_category() == Defs.JournalPublished:
        return journal_published_hr(reference)
    elif reference.get_category() == Defs.BookInPress:
        return book_inpress_hr(reference)
    elif reference.get_category() == Defs.ChapterInPress:
        return chapter_inpress_hr(reference)
    elif reference.get_category() == Defs.JournalInPress:
        return journal_inpress_hr(reference)


def book_published_amj(book):
    author_str = get_author_str(book.get_authors())
    title_str = book_title_filter(book.get_title())
    return "{0} {1}. {2}. {3}: {4}.".format(author_str, book.get_year(), title_str,
                                               book.get_location(),
                                               book.get_publisher())


def chapter_published_amj(chapter):
    author_str = get_author_str(chapter.get_authors())
    editor_str = get_reverse_editor_str(chapter.get_editors())
    return "{0} {1}. {2}. In {3}, <i><b>{4}</b></i>{5}: {6}. {7}: {8}.".format(author_str,
                                                                                  chapter.get_year(),
                                                                                  chapter.get_chapter_title(),
                                                                                  editor_str,
                                                                                  chapter.get_book_title(),
                                                                                  ", " + chapter.get_page_addition() if chapter.get_page_addition() else "",
                                                                                  chapter.get_start_page() + "–" + chapter.get_end_page(),
                                                                                  chapter.get_location(),
                                                                                  chapter.get_publisher())


def journal_published_amj(journal):
    author_str = get_author_str(journal.get_authors())
    return "{0} {1}. {2}. <i><b>{3}</b></i>, {4}{5}: {6}.".format(author_str, journal.get_year(), journal.get_title(),
                                                                  journal.get_journal(),
                                                                  journal.get_volume(),
                                                                  "(" + journal.get_issue() + ")" if journal.get_issue() else "",
                                                                  journal.get_start_page() + "–" + journal.get_end_page())


def book_inpress_amj(book):
    author_str = get_author_str(book.get_authors())
    title_str = book_title_filter(book.get_title())
    return "{0} {1}. {2}.".format(author_str, book.get_year(), title_str)


def chapter_inpress_amj(chapter):
    author_str = get_author_str(chapter.get_authors())
    editor_str = get_reverse_editor_str(chapter.get_editors())
    return "{0} {1}. {2}. In {3}, <i><b>{4}</b></i>.".format(author_str,
                                                             chapter.get_year(),
                                                             chapter.get_chapter_title(),
                                                             editor_str,
                                                             chapter.get_book_title())


def journal_inpress_amj(journal):
    author_str = get_author_str(journal.get_authors())
    return "{0} {1}. {2}. <i><b>{3}</b></i>.".format(author_str, journal.get_year(), journal.get_title(),
                                                     journal.get_journal())


def online_resources_amj(journal):
    author_str = get_author_str(journal.get_authors())
    journal_str = (("<i><b>" + journal.get_journal() + "</b></i>. ") if journal.get_journal() else "")
    return "{0} {1}. {2}. {3}Retrieved from {4}".format(author_str, journal.get_year(),
                                                        journal.get_title(),
                                                        journal_str,
                                                        journal.get_source())


def other_amj(journal):
    return journal.get_original()


def get_author_str(authors, cat1=", ", cat2=", & ", f_cat=". ", fl_cat=", "):
    author_str = authors[0].to_format_string(f_cat=f_cat, fl_cat=fl_cat)
    for author in authors[1:-1]:
        author_str += cat1 + author.to_format_string(f_cat=f_cat, fl_cat=fl_cat)
    if (len(authors)) > 1:
        author_str += cat2 + authors[-1].to_format_string(f_cat=f_cat, fl_cat=fl_cat)
    return author_str


def get_editor_str(editors, cat1=", ", cat2=" & ", eds=" (Eds.)", ed=" (Ed.)", f_cat=". ", fl_cat=", "):
    editor_str = editors[0].to_format_string(f_cat=f_cat, fl_cat=fl_cat)
    for editor in editors[1:-1]:
        editor_str += cat1 + editor.to_format_string(f_cat=f_cat, fl_cat=fl_cat)
    if (len(editors)) > 1:
        editor_str += cat2 + editors[-1].to_format_string(f_cat=f_cat, fl_cat=fl_cat) + eds
    else:
        editor_str += ed
    return editor_str


def get_reverse_editor_str(editors, cat1=", ", cat2=" & ", eds=" (Eds.)", ed=" (Ed.)", f_cat=". ", fl_cat=", "):
    editor_str = editors[0].to_reverse_format_string(f_cat=f_cat, fl_cat=fl_cat)
    for editor in editors[1:-1]:
        editor_str += cat1 + editor.to_reverse_format_string(f_cat=f_cat, fl_cat=fl_cat)
    if (len(editors)) > 1:
        editor_str += cat2 + editors[-1].to_reverse_format_string(f_cat=f_cat, fl_cat=fl_cat) + eds
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


def book_published_hr(book):
    author_str = get_author_str(book.get_authors(), cat1=", ", cat2=" and ", f_cat="", fl_cat=" ")
    title_str = book_title_filter(book.get_title(), bold=False, italic=True)
    return "{0} ({1}) {2}. {3}: {4}.".format(author_str, book.get_year(), title_str,
                                                book.get_location(),
                                                book.get_publisher())


def chapter_published_hr(chapter):
    author_str = get_author_str(chapter.get_authors(), cat1=", ", cat2=" and ", f_cat="", fl_cat=" ")
    editor_str = get_editor_str(chapter.get_editors(), ed=" (ed.)", eds=" (eds)", cat1=", ", cat2=", ", f_cat="",
                                fl_cat=" ")
    return "{0} ({1}) {2}. In: {3} <i>{4}</i>. {5}: {6}{7}, {8}.".format(author_str,
                                                                            chapter.get_year(),
                                                                            chapter.get_chapter_title(),
                                                                            editor_str,
                                                                            chapter.get_book_title(),
                                                                            chapter.get_location(),
                                                                            chapter.get_publisher(),
                                                                            ", " + chapter.get_page_addition() if chapter.get_page_addition() else "",
                                                                            chapter.get_start_page() + "–" + chapter.get_end_page()
                                                                            )


def journal_published_hr(journal):
    author_str = get_author_str(journal.get_authors(), cat1=", ", cat2=" and ", f_cat="", fl_cat=" ")
    return "{0} ({1}) {2}. <i>{3}</i> {4}{5}: {6}.".format(author_str, journal.get_year(), journal.get_title(),
                                                           journal.get_journal(),
                                                           journal.get_volume(),
                                                           "(" + journal.get_issue() + ")" if journal.get_issue() else "",
                                                           journal.get_start_page() + "–" + journal.get_end_page())


def book_inpress_hr(book):
    author_str = get_author_str(book.get_authors(), cat1=", ", cat2=" and ", f_cat="", fl_cat=" ")
    title_str = book_title_filter(book.get_title(), bold=False, italic=True)
    return "{0} ({1}) {2}.".format(author_str, book.get_year(), title_str)


def chapter_inpress_hr(chapter):
    author_str = get_author_str(chapter.get_authors(), cat1=", ", cat2=" and ", f_cat="", fl_cat=" ")
    editor_str = get_editor_str(chapter.get_editors(), ed=" (ed.)", eds=" (eds)", cat1=", ", cat2=", ", f_cat="",
                                fl_cat=" ")
    return "{0} ({1}) {2}. In: {3} <i>{4}</i>.".format(author_str,
                                                       chapter.get_year(),
                                                       chapter.get_chapter_title(),
                                                       editor_str,
                                                       chapter.get_book_title()
                                                       )


def journal_inpress_hr(journal):
    author_str = get_author_str(journal.get_authors(), cat1=", ", cat2=" and ", f_cat="", fl_cat=" ")
    return "{0} ({1}) {2}. <i>{3}</i>.".format(author_str, journal.get_year(), journal.get_title(),
                                               journal.get_journal())


def online_resources_hr(journal):
    author_str = get_author_str(journal.get_authors())
    journal_str = (("<i>" + journal.get_journal() + "</i>. ") if journal.get_journal() else "")
    return "{0} ({1}) {2}. {3}Available at: {4}".format(author_str, journal.get_year(),
                                                        journal.get_title(),
                                                        journal_str,
                                                        journal.get_source())


from Book import *
from Chapter import *
from Journal import *


def main():
    c_input = "Chen, G., Mathieu, J. E., & Bliese, P. D. (2004). A framework for conducting multilevel construct validation. In F. J. Yammarino & F. Dansereau (Eds.), Research in multilevel issues: Multilevel issues in organizational behavior and processes (Vol. 3, pp. 273–303). Oxford, UK: Elsevier. http://dx.doi.org/10.1016/S1475–9144(04)03013–9"
    b_input = "Matthews, G., Smith, Y., & Knowles, G. (2009). Disaster management in archives, libraries and museums. Farnham, England: Ashgate."
    j_input = "Avey, J. B., Wernsing, T. S., & Palanski, M. E. (2012). Exploring the process of ethical leadership: The mediating role of employee voice and psychological ownership. Journal of Business Ethics, 107, 21–34. http://dx.doi.org/10.1007/s10551–012–1298–2"

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
