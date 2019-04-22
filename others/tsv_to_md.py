import os
import sys
import re


def read_file_content(path):
    try:
        fp = open(path, "r")
        content = fp.read()
        return content
    except IOError:
        print("read file failed.")
        return


def main(path):
    if not os.path.isfile(path):
        print("The file '%s' is valid" % path)
        return

    content = read_file_content(path)
    print(content)
    print("\n==========================================\n")

    line1 = re.sub(r'(.+?)(\t|$)', r'----------\2', re.split(r'\n', content)[0])
    content = re.sub(r'(^.+)', r'\1\n' + line1 + '', content)
    markdown = re.sub(r'(.*)\n', r'|\1|\n', content)
    markdown = re.sub(r'\t', '|', markdown)

    markdown = re.sub(r'((\d+\.\d\d)\d+)', r'\2', markdown)

    print(markdown)


if __name__ == '__main__':
    main(sys.argv[1])
