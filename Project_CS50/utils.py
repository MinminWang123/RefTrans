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
    return extract_source(text)[1]


def get_clean_text(text):
    return extract_source(text)[0]


def main():
    # with open('Chapter.txt', 'r') as file:
    #     for line in file.readlines():
    #         print("clean:", get_clean_text(line))
    #         print("source:", get_source(line))
    #         print("---------")
    line = "Chen, G., Mathieu, J. E., & Bliese, P. D. (2004). A framework for conducting multilevel construct validation. In F. J. Yammarino & F. Dansereau (Eds.), Research in multilevel issues: Multilevel issues in organizational behavior and processes (Vol. 3, pp. 273-303). Oxford, UK: Elsevier. httpswww.//dx.doi.org/10.1016/S1475-9144(04)03013-9"
    print("clean:", get_clean_text(line))
    print("source:", get_source(line))



if __name__ == "__main__":
    main()
