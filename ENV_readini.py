#!/usr/bin/env python3

import sys
import os
import re
import pathlib
import argparse
from configparser import ConfigParser, ExtendedInterpolation
import types

# For testing purposes
import countnum

if sys.version_info < (3, 6):
    raise SystemExit("Require python 3.6")

##
# This program reads key-value list from an ini file and
# converts values to a windows or unix compatible path format
#
# This allows the a single ini config file to be used in
# set-environment scripts.
#
# The output of this program will either be applied by a batch file
# or a shell script, depending on the environment
# (msys/cygwin/git-bash or cmd/windows terminal)
#
# cygpath can do a similar thing, but was way to slow for my needs
##

__pathScript = pathlib.Path(__file__).parent.resolve()
__defaultIniName = "ENV.ini"


def toPathFormatUnix(envVarValue, _):
    envVarSanitized = envVarValue.replace("\\", "/").replace(" ", "\ ")
    envVarSanitized = re.sub(r"([A-Za-z]):", lambda m: "/"+m.group(1).lower(), envVarSanitized)
    envVarSanitized = envVarSanitized.replace(";", ":")
    return envVarSanitized

def toPathFormatMixed(envVarValue, _):
    return envVarValue.replace("\\", "/")


def convertPathFormat(varValue, pathFormat):
    return {
        "m": toPathFormatMixed,
        "u": toPathFormatUnix,
        "w": lambda p,_: p,
        None: lambda p,_: p,
    }[pathFormat](varValue, pathFormat)

def convertNameFormat(sectName, varName, nameFormat):
    return {
        "f": f"{sectName}:{varName}",
        "u": f"{sectName}_{varName}",
        "s": f"{varName}",
        None: f"",
    }[nameFormat]

def outputPrefixed(envVarName, envVarValue, prefix):
    parts = []
    if prefix:
        parts.append(prefix)
    if envVarName:
        parts.append("{}={}".format(envVarName, envVarValue))
    else:
        parts.append(envVarValue)

    print(" ".join(parts))

def convertEnvVariables(entries, sectName, queryVars, args):
    for name, val in entries.items():
        if "*" in queryVars or name in queryVars:
            val = convertPathFormat(val, args.pathFormat);
            name = convertNameFormat(sectName, name, args.nameFormat);
            outputPrefixed(name, val, args.prefix)


def resolveIniFile(inifilepath):
    if inifilepath is None:
        inifilepath = __defaultIniName
    filePath = pathlib.Path(inifilepath).resolve()
    if not filePath.is_file():
        filePath = pathlib.Path(__pathScript.joinpath(inifilepath)).resolve()
    if not filePath.is_file():
        return None
    return filePath


def loadIniFile(filePath):
    iniConfig = ConfigParser(interpolation=ExtendedInterpolation())
    iniConfig.optionxform = lambda option: option
    iniConfig.read(filePath)
    iniDict = {}
    for sectName in iniConfig.sections():
        sectCfg = iniConfig[sectName]
        sectDict = {}
        for iniEntryKey in sectCfg:
            sectDict[iniEntryKey] = sectCfg[iniEntryKey]
        iniDict[sectName] = sectDict

    # For testing purposes
    nameCountFile = "countReadIni.txt"
    countReadIniNr = countnum.readIncreaseWriteCount(nameCountFile)
    sectVARS_DEVENV = iniDict.setdefault("DEVENV_VARS", {})
    sectVARS_DEVENV["countReadIni"] = str(countReadIniNr)

    return iniDict


if __name__ == '__main__':

    class CustomHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
        """CustomHelpFormatter """

        def _format_action_invocation(self, action):
            if not action.option_strings:
                default = self._get_default_metavar_for_positional(action)
                metavar, = self._metavar_formatter(action, default)(1)
                return metavar

            parts = []

            # if the Optional doesn't take a value, format is:
            #    -s, --long
            if action.nargs == 0:
                parts.extend(action.option_strings)
                return ', '.join(parts)

            # if the Optional takes a value, format is:
            #    -s, --long ARGS
            default = self._get_default_metavar_for_optional(action)
            args_string = self._format_args(action, default)
            for option_string in action.option_strings:
                parts.append('%s' % option_string)
            return ', '.join(parts) + ' ' +args_string



    
    queryList = [
        "show", "list", "sections", "dump", "ls", "env"
    ]

    parser = argparse.ArgumentParser(
        formatter_class=CustomHelpFormatter,
        epilog="Print a list of .ini sections by using one of: "+str(queryList),
        description='Read ini file sections and print the set variabels, preparing for the destination environment.',
        allow_abbrev=True)

    parser.add_argument("-f", "--ini-file",
                        help="Path to ini file",
                        dest="inifile",
                        type=str,
                        default="ENV.ini")


    parser.add_argument("-t",'--path-format','--path-format2',
                        help="Set path format (mixed, unix, windows)",
                        dest="pathFormat",
                        type=str,
                        default="w",
                        choices=["n", "None", "m", "u", "w"])
    parser.add_argument("-n", '--name-format',
                        help="Set name format. (short, full, underscore)",
                        dest="nameFormat",
                        type=str,
                        default="s",
                        choices=["n", "None", "s", "f", "u"])

    parser.add_argument("-p", '--prefix',
                        help="Optional prefix (Prepend set or export)",
                        dest="prefix",
                        type=str,
                        default=None)

    parser.add_argument("-v", '--verbose',
                        help="Verbose output",
                        action='store_true', default=False)

    parser.add_argument(dest="query",
                        help="Sections/Variables to query",
                        nargs='*',
                        type=str,
                        action='store',
                        default=[])
    DEVPATH_ARGS = os.environ.get('DEVPATH_ARGS', None)
    mainArgs = sys.argv[1:]
    if DEVPATH_ARGS:
        TMP_ARGS = DEVPATH_ARGS.split(" ")
        TMP_ARGS.extend(mainArgs)
        mainArgs = TMP_ARGS

    args = parser.parse_args(mainArgs)
    if len(args.query) == 1 and len(args.query[0]) == 0:
        args.query = []

    if not len(args.query):
        parser.print_help()
        sys.exit(0)

    if args.nameFormat is not None:
        if args.nameFormat.lower() in ["none", "n", "-", ""]:
            args.nameFormat = None

    if args.verbose and DEVPATH_ARGS:
        print("Using environemt DEVPATH_ARGS '{}'".format(str(TMP_ARGS)))

    filePath = resolveIniFile(args.inifile)

    if not filePath:
        exit("Cannot find file {}".format(args.inifile))

    dictEnvVars = loadIniFile(filePath)


    if any(query in args.query for query in queryList):
        for sectName, entries in dictEnvVars.items():
            print("[{}]".format(sectName))
            # for key, val in entries.items():
            #     print("{}={}".format(key, val))
        exit(0)

    argsQuery = args.query

    queryMap = {}

    numMissing = 0
    for arg in argsQuery:
        argUpper = arg.upper()
        querySect, queryVar = (argUpper, "*") if not ":" in argUpper else argUpper.split(":", 1)
        # print(f"{querySect}->{queryVar}")
        found = False
        if querySect in dictEnvVars:
            queryMap.setdefault(querySect, set()).add(queryVar)
        else:
            numMissing += 1
            if args.verbose:
                print("'{}' not found".format(argUpper))

    for sectName, queryVars in queryMap.items():
        if sectName in dictEnvVars:
            if args.verbose:  # -v
                print("'{}' matches section".format(sectName))
            convertEnvVariables( dictEnvVars[sectName], sectName, queryVars, args)

    exit(numMissing)
