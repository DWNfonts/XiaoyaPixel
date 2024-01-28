#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# IDS Reader
# A library for reading IDS by Yi Bai.

# Copyright 2024 DWNfonts
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# History:
# Jan xx 2024: initial release

# There are 12 types (a-l) of a glyph's size.
# Duti chars (独体字) are "a" type such as 文, 龟, 木.
# Other glyphs can be describe via IDS can be converted:
# 相: ⿰木目 - 木 is b, 目 is c.
# 杏: ⿱木口 - 木 is d, 口 is e.
# Following, the outside part is always a.
# 回: ⿴囗口 - 口 (the inside part) is f.
# 凰: ⿵几皇 - 皇 is g.
# 凶: ⿶凵㐅 - 㐅 is h.
# 匠: ⿷匚斤 - 斤 is i.
# 病: ⿸疒丙 - 并 is j.
# 戒: ⿹戈廾 - 廾 is k.
# 超: ⿺走召 - 召 is l.
# 巫: ⿻工从 - both 工 and 从 are a.
# There's no conversion of ⿲ (衍: ⿲彳氵亍), ⿳ (京: ⿳亠口小), but they can be described via ⿰ and ⿱.
# ⿼ (㕚: ⿼叉丶), ⿽ (氷: ⿽水丶) is supported now.
# ⿾ (卐: ⿾卍), ⿿ (𠕄: ⿿凹), and ㇯ (乒: ㇯兵丶) are kept.

# Some glyphs won't fit when you strictly follow the method above.
# If there are more than 1 glyphs in one type in one char, there will be a varieties number following next to the type.
# the glyph name is coded as <Unicode codepoint> + <type> + <variety>.
# e.g. 劦 in 脇 (type c) → 52a6.c1; ⿰丬夕 in 桨 → 2ff0.4e2c.5915.d1

import list2str, re


def chr2ufn(strChar):
    # Char to Unicode Filename
    lstOutput = []
    for i in range(len(strChar)):
        lstOutput.append("%x" % ord(strChar[i]))
    return ".".join(lstOutput)


def splitIDS(strIDS):
    lstIDS = strIDS.split(";")
    dctOutput = {}
    for i in range(len(lstIDS)):
        strIDS = lstIDS[i]
        blnMatch = re.search(r"[^#]\(([U.HMTJKPVBS],)*[U.HMTJKPVBS]\)$", strIDS)
        # re.match doesn't work. IT'S THE MOST FREAKING THINGS THAT I KNOW.
        if blnMatch:
            a = len(strIDS) - strIDS[::-1].index("(") - 1
            # a here means the last item of "("
            # I don't use "re" to search it seems to be buggy
            # I use it to match it w/ (UGHMTJKPVBS)
            # https://stackoverflow.com/a/63834895
            strCountry = strIDS[a + 1 : -1]
            strContent = strIDS[:a]
            for j in strCountry.split(","):
                dctOutput[j.strip(")")] = strContent
        else:
            dctOutput["default"] = strIDS
    return dctOutput


def defaultIDS(preSpilt):
    dctSpilt = splitIDS(preSpilt)
    if "J" in dctSpilt:
        return dctSpilt["J"]
    elif "S" in dctSpilt:
        return dctSpilt["S"]
    elif "K" in dctSpilt:
        return dctSpilt["K"]
    elif "U" in dctSpilt:
        return dctSpilt["U"]
    elif "B" in dctSpilt:
        return dctSpilt["B"]
    elif "." in dctSpilt:
        return dctSpilt["."]
    elif "H" in dctSpilt:
        return dctSpilt["H"]
    elif "T" in dctSpilt:
        return dctSpilt["T"]
    else:
        return dctSpilt["default"]


def objectIDS(strIDS):
    # some components are:
    # #(xxx): a component which is too hard to describe via IDS, and it's not in Unicode;
    # [xxx]: describe the component next to it;
    # {xxx}: describe the component next to it.
    # these or "#[{" can be in the start of a IDS.
    blnBracket = False
    strBuffer = ""
    lstOutput = []
    for i in range(len(strIDS)):
        a = strIDS[i]
        strBuffer += a
        if a in "#[{":
            blnBracket = True
        if a == ")":
            blnBracket = False
        if strIDS[i - 1] in "]}":
            blnBracket = False
        if not blnBracket:
            lstOutput.append(strBuffer)
            strBuffer = ""
    return lstOutput


def partIDS(lstIDS, size):
    a = 1
    layer = 0
    lstOutput = []
    strBuffer = ""
    i = 0
    idc = lstIDS[i]
    lstOutput.append(idc)
    i += 1
    for j in range(size):
        comp = lstIDS[i]
        if comp[-1] in "⿾⿿":
            b = partIDS(lstIDS[i:], 1)
            lstOutput.append(b[0])
            i += b[1]
        elif comp[-1] in "⿰⿱⿴⿵⿶⿷⿸⿹⿺⿻⿼⿽":
            b = partIDS(lstIDS[i:], 2)
            lstOutput.append(b[0])
            i += b[1]
        elif comp[-1] in "⿲⿳":
            b = partIDS(lstIDS[i:], 3)
            lstOutput.append(b[0])
            i += b[1]
        else:
            lstOutput.append(comp)
            i += 1
    return (lstOutput, i)


def smartIDS(preIDS):
    strIDS = defaultIDS(preIDS)
    lstIDS = objectIDS(strIDS)
    idc = lstIDS[0][-1]

    def checkSize(idc):
        if idc in "⿾⿿":
            return 1
        if idc in "⿰⿱⿴⿵⿶⿷⿸⿹⿺⿻⿼⿽":
            return 2
        if idc in "⿲⿳":
            return 3
        else:
            return 0

    size = checkSize(idc)
    if size == 0:
        return None
    lstPreOutput = partIDS(lstIDS, size)[0]
    lstOutput = []
    # lstOutput = sum(lstPreOutput, [])
    # https://stackoverflow.com/a/716489
    for i in range(len(lstPreOutput)):
        entry = lstPreOutput[i]
        if isinstance(entry, str):
            lstOutput.append(entry)
        else:
            lstOutput.append(list2str.list2str(lstPreOutput[i]))
    return lstOutput


def toComp(ids):
    parted = smartIDS(ids)
    if parted == None:
        return None
    if len(parted) == 2:
        rawOutput = "".join(parted)
        return chr2ufn(rawOutput) + ".a"
    elif len(parted) == 4:
        # will be seen as ⿰X⿰YZ → X.b,⿰YZ.c#
        if parted[0] == "⿲":
            x = chr2ufn(parted[1])
            y = chr2ufn(parted[2])
            z = chr2ufn(parted[3])
            return "%s.b,2ff0.%s.%s.c#" % (x, y, z)
        elif parted[0] == "⿳":
            x = chr2ufn(parted[1])
            y = chr2ufn(parted[2])
            z = chr2ufn(parted[3])
            return "%s.d,2ff1.%s.%s.e#" % (x, y, z)
    elif len(parted) == 0:
        return None
    else:
        dctMagic = {
            "⿰": "bc",
            "⿱": "de",
            "⿴": "af",
            "⿵": "ag",
            "⿶": "ah",
            "⿷": "ai",
            "⿸": "aj",
            "⿹": "ak",
            "⿺": "al",
            "⿻": "am",
            "⿼": "an",
            "⿽": "ao",
        }
        compType = dctMagic[parted[0][-1]]
        xType = compType[0]
        yType = compType[1]
        x = chr2ufn(parted[1])
        y = chr2ufn(parted[2])
        return "%s.%s,%s.%s" % (x, xType, y, yType)
