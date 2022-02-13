#!/usr/bin/env python3
import pathlib
import traceback
import os
__pathScript = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))


def readCount(pathCountFile):
    count = 0
    try:
        if os.path.isfile(pathCountFile):
            with open(pathCountFile, "r") as fIn:
                lines = fIn.readlines()
                if len(lines):
                    count = int(lines[0])
    except Exception as exc:
        traceback.print_exc()
        print(exc)

    return count


def writeCount(pathCountFile, count):
    with open(pathCountFile, "w") as fOut:
        fOut.seek(0)
        fOut.write("%d\n" % count)
    return count


def readIncreaseWriteCount(nameCountFile):
    pathCountFile = os.path.join(__pathScript, nameCountFile)
    count = readCount(pathCountFile)
    writeCount(pathCountFile, count + 1)
    return count

def getAndIncreaseCount():
    nameCountFile = "countnumber.txt"
    currentNumber = readIncreaseWriteCount(nameCountFile)
    return currentNumber

if __name__ == '__main__':
    i = getAndIncreaseCount()
    print("%d" % i)
