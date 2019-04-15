#!/usr/bin/python

import os
import json

pack_name = 'pack.json'
pack = 'pack.py'
unpack = 'unpack.py'
packer = 'packer.py'


def pack_item(item):
    try:
        listing = os.listdir(item)
    except Exception as e:
        with open(item, 'r') as file:
            content = file.read()
        return {"type": "file", "name": item, "content": content}
    content = []
    for sub_item in listing:
        if sub_item[0] == '.' or \
           sub_item in [pack_name, pack, unpack, packer]:
            continue
        content.append(pack_item(item + '/' + sub_item))
    return {"type": "dir", "name": item, "content": content}


def unpack_item(item):
    if item['type'] == 'file':
        with open(item['name'], 'w') as file:
            file.write(item['content'])
    elif item['type'] == 'dir':
        if item['name'] is not '.':
            os.mkdir(item['name'])
        for sub_item in item['content']:
            unpack_item(sub_item)


def pack():
    with open(pack_name, 'w') as f:
        json.dump(pack_item("."), f)


def unpack():
    with open(pack_name, 'r') as f:
        unpack_item(json.load(f))


#def run():
#    parts = __file__.split('/')
#    file = parts[len(parts) - 1]
#    if file == 'pack.py':
#        pack()
#    elif file == 'unpack.py':
#        unpack()
#
#
#run()
pack()

