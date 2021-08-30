import os
import sys
# 导入核心的三个模块
from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
from androguard.core.analysis import analysis

def get_androguard_obj(apkfile):
    a = apk.APK(apkfile)#获取APK文件对象
    d = dvm.DalvikVMFormat(a.get_dex())#获取DEX文件对象
    dx = analysis.Analysis(d)#获取分析结果对象
    return (a,d,dx)

sp = 'D:\\workspace\\Android-immunity\\androguard_attempt\\19300240012.apk'
# sp = 'D:\\文件\\学习\\课程\\曦源项目\\mwallet\\com.telkom.mwallet_101_apps.evozi.com.apk'
if __name__=='__main__':
    
    a, d, dx = get_androguard_obj(sp)
    strs =  dx.get_strings()
    print(strs)
    for str in strs:
        print(str.get_value())
    # for pkg in pkgs:
    #     print(pkg)#打印package name
