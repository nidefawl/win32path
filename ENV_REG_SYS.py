#!/usr/bin/env python3

import winreg as reg

# print environment variables from registry (MACHINE) 

args = [ reg.HKEY_LOCAL_MACHINE, "SYSTEM\CurrentControlSet\Control\Session Manager\Environment" ]
# print(r"HKEY_LOCAL_MACHINE/SYSTEM/CurrentControlSet/Control/Session Manager/Environment")
kHandle = reg.CreateKey(*args)
kSubCount, kNumValues, time = reg.QueryInfoKey(kHandle)
kValues = []
for i in range(kNumValues):
    vals = reg.EnumValue(kHandle, i)
    print("%32s %s"%(vals[0], str(vals[1])))
reg.CloseKey(kHandle)