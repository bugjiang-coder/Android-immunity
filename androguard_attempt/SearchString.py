import os
import sys
# 导入核心的三个模块
from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
from androguard.core.analysis import analysis
from textblob import TextBlob


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

    # 获取所有的string
    strs = dx.get_strings()

    cnt = 1  # 输出计数
    # 输出处理结果
    fout = open(".\\output_pos.txt", "w")
    for s in strs:
        blob = TextBlob(str(s.get_value()))
        if len(blob.tags)>=4 and blob.sentences[0].sentiment.polarity > 0:
            print("[%d]%s || %f" % (cnt, s.get_value(),blob.sentences[0].sentiment.polarity))
            fout.write("[%d]%s || %f" % (cnt, s.get_value(),blob.sentences[0].sentiment.polarity))
            # fout.write("["+str(cnt)+"]"+str(s.get_value()))

            cnt += 1

            for call in s.get_xref_from():
                # 打印谁调用了该string
                fout.write("\n\t"+str(call))

            fout.write('\n')

    fout.close()
