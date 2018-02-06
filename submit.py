#!/usr/bin/env python

import os
import sys
import time
import requests


wordbook_id = 180058

full_msg = u"\u8bcd\u4e32\u4e2d\u5355\u8bcd\u6570\u91cf\u8d85\u8fc7\u4e0a\u9650\uff0c\u65e0\u6cd5\u6dfb\u52a0\u5355\u8bcd"

cookies = {
    'csrftoken': '',
    '_ga': '',
    'auth_token': '',
    'sessionid': '',
    'userid': '',
}


def create_wordlist(name, description):
    print("create", name, description)

    headers = {
        'Host': 'www.shanbay.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.shanbay.com/wordbook/' + str(wordbook_id) + '/',
        'Connection': 'keep-alive',
    }

    data = [
        ('name', name),
        ('description', description),
        ('wordbook_id', str(wordbook_id)),
    ]

    r = requests.post('https://www.shanbay.com/api/v1/wordbook/wordlist/', headers=headers, cookies=cookies, data=data)
    print r.json()
    id = r.json()['data']['wordlist']['id']
    return id


def update_wordlist(id, name, description):
    print("update", id, name, description)
    headers = {
        'Host': 'www.shanbay.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.shanbay.com/wordbook/' + str(wordbook_id) + '/',
        'Connection': 'keep-alive',
    }

    data = [
        ('name', name),
        ('description', description),
        ('wordbook_id', str(wordbook_id)),
    ]

    r = requests.put('https://www.shanbay.com/api/v1/wordlist/' + str(id) + '/', headers=headers, cookies=cookies, data=data)
    print(r.json())


def add_word(id, word):
    print("addword", id, word)

    headers = {
        'Host': 'www.shanbay.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.shanbay.com/wordlist/' + str(wordbook_id) + '/' + str(id) + '/',
        'Connection': 'keep-alive',
    }

    data = [
        ('id', str(id)),
        ('word', word),
    ]

    r = requests.post('https://www.shanbay.com/api/v1/wordlist/vocabulary/', headers=headers, cookies=cookies, data=data)
    print(r.json())
    return r.json()


def process_file(file_path):
    print(file_path)
    file_name = os.path.basename(file_path)
    wordbook_name = file_name.replace('_words.log', '')

    id = create_wordlist(wordbook_name, wordbook_name)

    wordbook_index = 1
    success_words = []
    failed_words = []

    with open(file_path) as f:
        words = f.readlines()
        for word in words:
            word = word.strip()
            result = add_word(id, word)
            if result['msg'] == full_msg:
                if wordbook_index == 1:
                    update_wordlist(id, wordbook_name + str(wordbook_index), wordbook_name)
                wordbook_index = wordbook_index + 1
                id = create_wordlist(wordbook_name + str(wordbook_index), wordbook_name)
                result = add_word(id, word)
            
            if result['status_code'] == 0:
                success_words.append(word)
            else:
                failed_words.append(word)

    with open(os.path.join(os.path.dirname(file_path), wordbook_name + "_words.result"), 'w') as f:
        f.write("Added:\n")
        f.write(" ".join(success_words))
        f.write("\n-------------------------------\n")
        f.write("Not added\n")
        f.write(" ".join(failed_words))


def main():
    if len(sys.argv) != 2:
        print("You must specify directory!")
        exit(1)

    target_dir = os.path.abspath(sys.argv[1])

    for root, dirs, files in os.walk(target_dir):
        for name in files:
            if not name.endswith(".log"):
                continue
            process_file(os.path.join(root, name))


if __name__ == "__main__":
    main()
