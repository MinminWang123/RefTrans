import re


def extract_source(text):
    clean_text = re.match('(.*?)([Dd][Oo][Ii]:.*)', text)
    if clean_text:
        return clean_text.group(1), clean_text.group(2)

    clean_text = re.match('(.*?)((http.*)|(www\..*))', text)
    if clean_text:
        return clean_text.group(1), clean_text.group(2)
    return text, ""


def get_source(text):
    return extract_source(text)[1].strip()


def get_clean_text(text):
    return extract_source(text)[0].strip()


def get_body(text):
    try:
        body = re.search("\)\.(.*)", get_clean_text(text)).group(1).strip()
    except AttributeError:
        body = None
    return body


def shrink_page(sp, ep):
    sp = str(sp)
    ep = str(ep)
    if len(ep) <= 2:
        return ep
    if sp[0] != ep[0]:
        return ep
    if sp[1] != ep[1]:
        return ep[1:]
    if sp[2] != ep[2]:
        return ep[2:]
    else:
        return ep[2:]


def main():
    # with open('Chapter.txt', 'r') as file:
    #     for line in file.readlines():
    #         print("clean:", get_clean_text(line))
    #         print("source:", get_source(line))
    #         print("---------")
    # line = "Chen, G., Mathieu, J. E., & Bliese, P. D. (2004). A framework for conducting multilevel construct validation. In F. J. Yammarino & F. Dansereau (Eds.), Research in multilevel issues: Multilevel issues in organizational behavior and processes (Vol. 3, pp. 273-303). Oxford, UK: Elsevier. httpswww.//dx.doi.org/10.1016/S1475-9144(04)03013-9"
    # print("clean:", get_clean_text(line))
    # print("source:", get_source(line))
    # print("body: ", get_body(line))
    print(shrink_page(1, 46))



if __name__ == "__main__":
    main()
