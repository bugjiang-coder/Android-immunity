import os
import sys
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

# 输出所有字符串
def output_calling_method(strs):
    cnt = 1  # 输出计数
    # 输出处理结果
    fout = open(".\\output.txt", "w",encoding='utf-8')
    for s in strs:
        text = str(s.get_value())
        blob = TextBlob(text)
        score = blob.sentiment.polarity

        fout.write("[%d]%s || %f" % (cnt, text, score))
        cnt += 1
        for call in s.get_xref_from():
            try:
                fout.write("\n\t"+str(call))
            except:
                print("write error")

        fout.write('\n\n')

    fout.close()

def output_calling_method_pos(strs):
    cnt = 1
    fout_p = open(".\\output_pos.txt", "w",encoding='utf-8')

    for s in strs:
        text = str(s.get_value())
        blob = TextBlob(text)
        score = blob.sentiment.polarity
        if len(blob.words) >= 4:
            if score > 0:
                fout_p.write("[%d]%s || %f" % (cnt, text, score))
                cnt += 1
                for call in s.get_xref_from():
                    # 打印谁调用了该string
                    try:
                        fout_p.write("\n\t"+str(call))
                    except:
                        print("write error")
                fout_p.write('\n\n')

    fout_p.close()

def output_calling_method_neg(strs):
    cnt = 1
    fout_n = open(".\\output_neg.txt", "w",encoding='utf-8')

    for s in strs:
        text = str(s.get_value())
        blob = TextBlob(text)
        score = blob.sentiment.polarity
        if len(blob.words) >= 4:
            if score < 0:
                fout_n.write("[%d]%s || %f" % (cnt, text, score))
                cnt += 1
                for call in s.get_xref_from():
                    # 打印谁调用了该string
                    try:
                        fout_n.write("\n\t"+str(call))
                    except:
                        print("write error")
                fout_n.write('\n\n')

    fout_n.close()

def output_arsc_strings(a):
    arscobj = a.get_android_resources()
    if not arscobj:
        print("The APK does not contain a resources file!")
        return
    
    fout_s = open(".\\output_arsc.txt", "w",encoding='utf-8')
    strings = arscobj.get_resolved_strings()
    for pkg in strings:
        if pkg ==  a.get_package():#只输出该报名下的string
            fout_s.write(pkg + ":\n")
            for locale in strings[pkg]:
                if locale ==  'DEFAULT':
                    for s in strings[pkg][locale]:
                        fout_s.write(str(s) +'\t'+strings[pkg][locale][s] + '\n')
                    # 只输出默认语言的strings.xml文件 s为string的id 右边为string
                    # eg:
                    # 2131427331      Navigate up
                    # 2131427332      More options
                    # 2131427333      Done
    fout_s.close()
                    



# 要分析的apk路径
# sp = 'D:\\workspace\\Android-immunity\\androguard_attempt\\19300240012.apk'
sp = 'D:\\文件\\学习\\课程\\曦源项目\\mwallet\\com.telkom.mwallet_101_apps.evozi.com.apk'

if __name__ == '__main__':
    # 处理apk
    a, d, dx = get_androguard_obj(sp)

    # 获取所有的string
    strs = dx.get_strings()

    output_calling_method(strs)
    output_calling_method_neg(strs)
    output_calling_method_pos(strs)

    output_arsc_strings(a)
    

