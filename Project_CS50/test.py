def write(line):
    with open("utf.txt", "a", encoding="utf-8") as csvfile:
        csvfile.write(line)
#
#
# with open("temp.txt", "r") as file:
#     for line in file.readlines():
#         write(line.strip("\n"))

with open("category.txt", "r") as file:
    for line in file.readlines():
        write(line)