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
# sp = 'D:\\workspace\\Android-immunity\\androguard_attempt\\19300240012.apk'
sp = 'D:\\文件\\学习\\课程\\曦源项目\\mwallet\\com.telkom.mwallet_101_apps.evozi.com.apk'

if __name__ == '__main__':
    # 处理apk
    a, d, dx = get_androguard_obj(sp)

    # 获取所有的string
    strs = dx.get_strings()

    cnt1 = 1  # 输出计数
    cnt2 = 1
    cnt3 = 1
    # 输出处理结果
    fout = open(".\\output.txt", "w")
    fout_n = open(".\\output_neg.txt", "w")
    fout_p = open(".\\output_pos.txt", "w")

    for s in strs:
        text = str(s.get_value())
        blob = TextBlob(text)
        score = blob.sentiment.polarity

        fout.write("[%d]%s || %f" % (cnt1, text, score))
        cnt1 += 1
        for call in s.get_xref_from():
            # print(call.get_method().source())
            # 打印谁调用了该string
            try:
                fout.write("\n\t"+str(call))
            except:
                print("error1")
            
        fout.write('\n\n')

        if len(blob.words) >= 4:
            if score > 0:
                fout_p.write("[%d]%s || %f" % (cnt2, text, score))
                cnt2 += 1
                for call in s.get_xref_from():
                    # 打印谁调用了该string
                    try:
                        fout_p.write("\n\t"+str(call))
                    except:
                        print("error2")
                fout_p.write('\n\n')

            elif score < 0:
                fout_n.write("[%d]%s || %f" % (cnt3, text, score))
                cnt3 += 1
                for call in s.get_xref_from():
                    try:
                    # 打印谁调用了该string
                        fout_n.write("\n\t"+str(call))
                    except:
                        print("error")
                fout_n.write('\n\n')

    fout.close()
    fout_n.close()
    fout_p.close()
