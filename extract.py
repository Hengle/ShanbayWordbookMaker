#!/usr/bin/env python

import os
import re
import sys


ordered = False


def process(file_path):
    print(file_path)
    word_set = read_file(file_path)
    write_file(file_path, word_set)
    return word_set


def read_file(file_path):
    with open(file_path) as f:
        content = f.read()
        word_list = re.sub("[^\w]", " ", content.lower()).split()
        if ordered:
            word_set = list(set(word_list))
            word_set.sort()
        else:
            word_set = set(word_list)
        return word_set


def write_file(file_path, word_set):
    file_name = os.path.basename(file_path)
    word_file_path = os.path.join(os.path.dirname(file_path), os.path.splitext(file_name)[0] + "_words.log")
    content = "\n".join(word_set)
    with open(word_file_path, "w") as f:
        f.write(content)


def main():
    if len(sys.argv) != 2:
        print("You must specify directory!")
        exit(1)

    target_dir = os.path.abspath(sys.argv[1])

    all_words = []
    for root, dirs, files in os.walk(target_dir):
        for name in files:
            if not name.endswith(".txt"):
                continue
            word_set = process(os.path.join(root, name))
            all_words.extend(word_set)

    all_words = list(set(all_words))
    all_words.sort()

    with open(os.path.join(target_dir, "Total.log"), "w") as f:
        f.write("\n".join(all_words))


if __name__ == "__main__":
    main()
