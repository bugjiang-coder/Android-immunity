from androguard.core.bytecodes.apk import APK
from androguard.core.bytecodes.dvm import DalvikVMFormat
from androguard.core.analysis.analysis import Analysis
from androguard.core.androconf import show_logging
import logging
# Enable log output
show_logging(level=logging.INFO)
# Load our example APK
a = APK("D:\\workspace\\Android-immunity\\androguard_attempt\\19300240012.apk")
# Create DalvikVMFormat Object
d = DalvikVMFormat(a)
# Create Analysis Object
dx = Analysis(d)
# 这里需要创建一下交叉引用
dx.create_xref()

strs =  dx.get_strings()
# print(strs)
cnt = 1
for str in strs:
    print("[",cnt,"]",str.get_value(),':')

    cnt += 1

    for call in str.get_xref_from():
        print(call)
    
    print('\n')
