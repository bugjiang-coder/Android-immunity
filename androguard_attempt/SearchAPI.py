# 导入核心的三个模块
from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
from androguard.core.analysis import analysis
from textblob import TextBlob

# 对apk进行处理
def get_androguard_obj(apkfile):
    a = apk.APK(apkfile)  # 获取APK文件对象
    d = dvm.DalvikVMFormat(a.get_dex())  # 获取DEX文件对象
    dx = analysis.Analysis(d)  # 获取分析结果对象
    dx.create_xref()  # 这里需要创建一下交叉引用
    return (a, d, dx)


# 要分析的apk路径
sp = 'D:\\workspace\\Android-immunity\\androguard_attempt\\19300240012.apk'
# sp = 'D:\\文件\\学习\\课程\\曦源项目\\mwallet\\com.telkom.mwallet_101_apps.evozi.com.apk'

if __name__ == '__main__':
    # 处理apk
    a, d, dx = get_androguard_obj(sp)
    
    dx.find_methods(classname="^(?!Landroid).*;$", methodname="<init>", descriptor=r"^\(.+\).*$")




    

