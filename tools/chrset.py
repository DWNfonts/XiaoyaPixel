#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Charset generator
# make union set of GB/T 2312, 现代汉语通用字表, 通用规范汉字表, and JIS kanji level 1-2.
# IMPORTING IS NOT RECOMMENDED

import json, sys

# fetch kTGH charset from Unihan database

kTGHset = []
with open('Unihan_OtherMappings.txt', 'r') as f:
    for line in f:
        if line.startswith('U+'):
            lstEntry = line.split('\t')
            strEncoding = lstEntry[0]
            strTag = lstEntry[1]
            if strTag == 'kTGH':
                strHanzi = eval('chr(%s)' % strEncoding.replace('U+', '0x'))
                kTGHset.append(strHanzi)

g7set = []
with open('g7.json', 'r', encoding='UTF-8') as f:
    objG7 = json.load(f)
    for lstHanziMeta in objG7['rows']:
        strHanzi = lstHanziMeta[1]
        g7set.append(strHanzi)

g0set = []
# https://en.wikipedia.org/wiki/GB_2312
# the range of Hanzi:
# pt. 1: [B0-D6][A1-FE]
# pt. 2: D7[A1-F9]
# pt. 3: [D8-F7][A1-FE]

for i in range(0xB0, 0xF8):
    for j in range(0xA1, 0xFF):
        encHanzi = i * 256 + j
        if encHanzi in range(0xD7FA, 0xD7FF):
            break # 0xD7FA - 0xD7FE are not Hanzi
        else:
            strHanzi = encHanzi.to_bytes(2, 'big').decode(encoding='GB2312')
            g0set.append(strHanzi)

j0set = []
# https://en.wikipedia.org/wiki/GB_2312
# exactly the same as the G0 one:
# break CFD4-CFFE

for i in range(0xB0, 0xF5):
    for j in range(0xA1, 0xFF):
        encHanzi = i * 256 + j
        if encHanzi in range(0xCFD4, 0xCFFF):
            break
        elif encHanzi in range(0xF4A6, 0xF4FF):
            break
        else:
            strHanzi = encHanzi.to_bytes(2, 'big').decode(encoding='EUC-JP')
            j0set.append(strHanzi)

allHanzi = set()
allHanzi = allHanzi.union(set(kTGHset))
allHanzi = allHanzi.union(set(g7set))
allHanzi = allHanzi.union(set(g0set))
allHanzi = allHanzi.union(set(j0set))

def write2file(filePath):
    f = open(filePath, 'w', encoding='UTF-8')
    f.write(''.join(allHanzi))

if len(sys.argv) < 2:
    AskedFilePath = input("Where to save? ")
    write2file(AskedFilePath)
else:
    write2file(sys.argv[1])