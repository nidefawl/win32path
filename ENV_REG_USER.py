#!/usr/bin/env python3

import winreg as reg

# print environment variables from registry (USER) 

args = [ reg.HKEY_CURRENT_USER, "Environment" ]
# print("HKEY_CURRENT_USER/Environment")
kHandle = reg.OpenKey(*args)
kSubCount, kNumValues, time = reg.QueryInfoKey(kHandle)
kValues = []
for i in range(kNumValues):
    vals = reg.EnumValue(kHandle, i)
    print("%32s %s"%(vals[0], str(vals[1])))
reg.CloseKey(kHandle)