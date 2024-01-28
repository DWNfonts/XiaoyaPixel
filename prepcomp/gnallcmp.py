#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# GenComps
# Generate components to XiaoyaPixel

# Copyright 2024 DWNfonts
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# NOT FOR IMPORTING, USING ONLY FOR COMMAND LINE

# History:
# Jan xx 2024: initial release

import idsread as ir
import sys

with open("charlist.txt", encoding="UTF-8") as file:
    charList = file.read()
with open("ids_lv2.txt", encoding="UTF-8") as f:
    with open("comps.txt", "w", encoding="UTF-8") as g:
        for line in f:
            lstLine = line.split("\t")
            entry = lstLine[0]
            ziLiIDS = ir.defaultIDS(lstLine[1])
            if entry in charList:
                toOutput = ir.toComp(ziLiIDS)
                if toOutput != None:
                    g.write("%s\t%s\n" % (entry, toOutput))
                else:
                    g.write("%s\t%s.a\n" % (entry, ir.chr2ufn(entry)))
with open("comps.txt", "r", encoding="UTF-8") as f:
    with open("comps1.txt", "w", encoding="UTF-8") as g:
        lstBuffer = []
        for line in f:
            lstLine = line.split("\t")
            entry = lstLine[0]
            lstComps = lstLine[1].strip("\n").split(",")
            for item in lstComps:
                if item not in lstBuffer:
                    g.write(item + "\n")
                lstBuffer.append(item)

with open("comps1.txt") as f:
    with open("compsr.txt", "w", encoding="UTF-8") as g:
        for line in f:
            comps = line.split(".")
            strCompReadable = ""
            for comp in comps:
                try:
                    numUni = eval("0x" + comp)
                    if numUni in range(0xA, 0x10):
                        strCompReadable += comp
                    else:
                        strCompReadable += chr(numUni)
                except:
                    strCompReadable += comp
            strCompReadable = strCompReadable.strip("\n")
            searchLine = line.strip("\n")
            hanziDetected = ""
            with open("comps.txt", encoding="UTF-8") as file:
                for entry in file:
                    if searchLine in entry:
                        hanziDetected += entry.split("\t")[0]
            g.write("%s\t%s\t%s\n" % (searchLine, strCompReadable, hanziDetected))
