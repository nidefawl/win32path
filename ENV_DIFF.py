#!/usr/bin/env python3

import winreg as reg
import os
from pprint import pprint as pp
import itertools as it
# read environment variables from registry (USER+MACHINE) 
# and compare it os.environ

PATH_VARS=('PATH', 'PSMODULEPATH')

envMapCurrent = {k: v.replace("\\", "/") for k, v in os.environ.items()}

envMapDefault = {}

args = [ reg.HKEY_LOCAL_MACHINE, "SYSTEM\CurrentControlSet\Control\Session Manager\Environment" ]

kHandle = reg.CreateKey(*args)
kSubCount, kNumValues, time = reg.QueryInfoKey(kHandle)
kValues = []
for i in range(kNumValues):
    vals = reg.EnumValue(kHandle, i)
    value = str(vals[1])
    if (vals[2] == reg.REG_EXPAND_SZ and vals[1] != 'PSModulePath'):
        value = reg.ExpandEnvironmentStrings(value)
    value = value.replace("\\", "/")
    key = vals[0]
    if key.upper() in PATH_VARS:
        key = key.upper()
    envMapDefault[key] = value
reg.CloseKey(kHandle)

args = [ reg.HKEY_CURRENT_USER, "Environment" ]
kHandle = reg.OpenKey(*args)
kSubCount, kNumValues, time = reg.QueryInfoKey(kHandle)
kValues = []
for i in range(kNumValues):
    vals = reg.EnumValue(kHandle, i)
    # key = vals[0].upper()
    key = vals[0]
    value = str(vals[1])
    if (vals[2] == reg.REG_EXPAND_SZ):
        value = reg.ExpandEnvironmentStrings(value)
    value = value.replace("\\", "/")
    if key.upper() in PATH_VARS:
        key = key.upper()
    if key in envMapDefault and key in PATH_VARS:
        envMapDefault[key] = (value + ';' + envMapDefault[key]).replace(';;', ';')
    else:
        envMapDefault[key] = value
reg.CloseKey(kHandle)



def parsePathVar(pathsvar):
    pathlist = pathsvar.split(';')
    pathlist.sort()
    return pathlist

def difflist(a, b):
    xa = [i for i in set(a) if i not in b]
    xb = [i for i in set(b) if i not in a]
    xa.sort()
    xb.sort()
    return {'-': xa, '+': xb}


def calcEnvDifference(left, right):
    diff = {x: dict() for x in ('diff', *PATH_VARS)}

    diff['-'] = {k: left[k] for k in (set(left) - set(right))}
    diff['+'] = {k: right[k] for k in (set(right) - set(left))}

    diffs = [k for k in set(left) & set(right) if left[k] != right[k]]

    for k in diffs:
        if k in PATH_VARS:
            pathLists = [parsePathVar(v) for v in (left[k], right[k])]
            diff[k] = difflist(*pathLists)
        else:
            diff['diff'][k] = {'-': left[k], '+': right[k]}
    return diff

envDiff = calcEnvDifference(envMapDefault, envMapCurrent)
pp(envDiff)