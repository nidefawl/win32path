#!/usr/bin/env python3

import argparse
import subprocess
import sys
import logging

# ninja -t deps output looks like this
#
# target: [other information we don't need]
#     some_file.cpp
#     some_header.h
#     other_header.h
# This program will print all headers included by a source file
# Or reverse: Print all source files that include a header

def mainCheckHeaders():
    parser = argparse.ArgumentParser(
        description='List all source files that include a header.')
    parser.add_argument("-r", "--source",
                        help="List all headers included by a specific source file",action='store_true')
    parser.add_argument("--header",
                        help=parser.description+" (default)",action='store_true')
    parser.add_argument("-q", "--summary",
                        help="Only print a per file summary. Do not list includes/sources",action='store_true')
    parser.add_argument("-s", "--sort-ascending",
                        help="Sort by number of includes/sources (ascending)",action='store_true')
    parser.add_argument("-S", "--sort-descending",
                        help="Sort by number of includes/sources (descending)",action='store_true')
    parser.add_argument('targetnames', help="names to search", nargs=argparse.REMAINDER)

    parser.add_argument("-C", "--build-dir",
                        help="Build directory (default cwd)")
    parser.add_argument("-f", "--build-file",
                        help="Build directory (default build.ninja)")

    if len(sys.argv) < 2:
        sys.argv = [__file__, '-h']
    args = parser.parse_args()

    ninja_prefix = ["ninja"]
    if args.build_dir is not None:
        ninja_prefix.extend(["-C", args.build_dir])
    if args.build_file is not None:
        ninja_prefix.extend(["-f", args.build_file])

    sortDirection = 0
    if args.sort_ascending:
        sortDirection = 1
    if args.sort_descending:
        sortDirection = -1
    mapBySource = 0
    if args.source:
        mapBySource = 1
    if args.header:
        mapBySource = 0

    srcToParent = {}
    parentToSrc = {}

    # print(len(srcToParent), "source to obj mappings")
    # print(len(parentToSrc), "obj to source mappings")

    # Fetch the cached dependency data
    curTarget = None
    headersTarget = []
    srcToHeaders = {}
    headersToSrc = {}
    ninja_deps_output = subprocess.check_output(ninja_prefix + ["-t", "deps"]).decode("UTF-8")
    if not ninja_deps_output.strip():
        print('ninja -t deps: Empty output, try building first')
    ninja_target_deps = (ninja_deps_output.splitlines());
    ninja_target_deps.append(":")
    for line in ninja_target_deps:
        if line.startswith("    "):
            dep = line[4:]
            assert curTarget is not None, "Source file appeared before target"
            headersTarget.append(dep)
        elif ":" in line:
            if curTarget is not None:
                # TODO: handle targets with multiple sources
                targetSources = [curTarget]

                headersTarget = [h for h in headersTarget if h not in targetSources]

                for targetsrc in targetSources:
                    srcToHeaders[targetsrc] = headersTarget
                for targetHeader in headersTarget:
                    if targetHeader not in headersToSrc:
                        headersToSrc[targetHeader] = []
                    headersToSrc[targetHeader].extend(targetSources)

            headersTarget = []
            curTarget = line.split(":", 1)[0]
            if curTarget.endswith(".obj"):
              curTarget = curTarget[:-4]


    srcMap =  [headersToSrc, srcToHeaders][mapBySource]
    strDesc = [ "{fmtNumMatched} sources include {fmtFilename}",
                "{fmtNumMatched} headers included by {fmtFilename}" ][mapBySource]
    matchList = []
    for srcName,srcList in srcMap.items():
        if not args.targetnames or any(x in srcName for x in args.targetnames):
            matchList.append((len(srcList), srcName))
    
    if sortDirection != 0:
        matchList = sorted(matchList, key=lambda x: x[0], reverse = sortDirection < 0)
    
    for numMapped, filenameMatched in matchList:
        print(strDesc.format(fmtNumMatched = numMapped, fmtFilename = filenameMatched))
        if not args.summary:
            for srcFile in srcMap[filenameMatched]:
                print(srcFile)

if __name__ == '__main__':
    mainCheckHeaders()
