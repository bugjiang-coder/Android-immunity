import os
import sys
# 导入核心的三个模块
from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
from androguard.core.analysis import analysis
from androguard import misc
from androguard import session
from textblob import TextBlob
from snownlp import SnowNLP

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
    fout = open(store_file_path+"output.txt", "w+", encoding='utf-8')
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
    fout_p = open(store_file_path+"output_pos.txt", "w", encoding='utf-8')

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


# 检验是否全是中文字符
def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


def output_calling_method_neg(strs):
    cnt = 1
    fout_n = open(store_file_path+"output_neg.txt", "w+", encoding='utf-8')

    for s in strs:
        # 使用TextBlob处理
        text = str(s.get_value())
        # in order to fliter some unimportant words
        if(len(text) <= 4):
            continue
        if not is_all_chinese(text):
            # print("English text:" + text)
            # os.system("pause")
            blob = TextBlob(text)
            score = blob.sentiment.polarity
            if score < 0:
                fout_n.write("[%d]%s || %f" % (cnt, text, score))
                cnt += 1
                for _, meth in s.get_xref_from():
                    # 打印谁调用了该string
                    try:
                        fout_n.write(
                            "\n\tUsed in {} -- {}".format(meth.class_name, meth.name))
                    except:
                        print("write error")
                fout_n.write('\n\n')
        # 使用SnowNLP分析
        else:
            snow = SnowNLP(text)
            score2 = snow.sentiments
            if(score2 < 0.3):  # 0表示不开心，1表示开心
                fout_n.write("[%d]%s || %f" % (cnt, text, score2))
                cnt += 1
                for _, meth in s.get_xref_from():
                    # 打印谁调用了该string
                    try:
                        fout_n.write(
                            "\n\tUsed in {} -- {}".format(meth.class_name, meth.name))
                    except:
                        print("write error")
                fout_n.write('\n\n')

    fout_n.close()


def output_arsc_strings(a):
    arscobj = a.get_android_resources()
    arsc_str = []
    arsc_str_id = []
    if not arscobj:
        print("The APK does not contain a resources file!")
        return

    fout_s = open(store_file_path+"output_arsc.txt", "w+", encoding='utf-8')
    strings = arscobj.get_resolved_strings()
    for pkg in strings:
        if pkg == a.get_package():  # 只输出该包名下的string
            fout_s.write(pkg + ":\n")
            for locale in strings[pkg]:
                if locale == 'DEFAULT':
                    for s in strings[pkg][locale]:

                        text = str(strings[pkg][locale][s])
                        if(len(text) <= 4):
                            continue

                        elif not is_all_chinese(text):
                            blob = TextBlob(text)
                            score = blob.sentiment.polarity
                            # 下面对消极的字符串进行处理
                            if score < -0.4:

                                fout_s.write(
                                    str(s) + '\t'+str(strings[pkg][locale][s]) + '\n')
                                # 加上arsc中的字符串
                                arsc_str.append(str(strings[pkg][locale][s]))
                                arsc_str_id.append(str(s))

                        else:
                            snow = SnowNLP(text)
                            score2 = snow.sentiments
                            if(score2 < 0.3):  # 0表示不开心，1表示开心
                                fout_s.write(
                                    str(s) + '\t'+str(strings[pkg][locale][s]) + '\n')
                                # 加上arsc中的字符串
                                arsc_str.append(str(strings[pkg][locale][s]))
                                arsc_str_id.append(str(s))

    fout_s.close()
    return arsc_str_id


# 要分析的apk路径
# file_path = 'D:\\workspace\\Android-immunity\\androguard_attempt\\19300240012.apk'
file_path = 'D:\\文件\\学习\\课程\\曦源项目\\mwallet\\com.telkom.mwallet_101_apps.evozi.com.apk'
# file_path = "C:\\Users\\86157\\Desktop\\Andguard\\lgeha.apk"
store_file_path = "D:\\workspace\Android-immunity\\androguard_attempt\\9-17"
smali_file_path = "D:\\workspace\Android-immunity\\androguard_attempt\\9-17\\smali_out"
work_file_path = "D:\\workspace\\Android-immunity\\androguard_attempt"


if __name__ == '__main__':
    # 处理apk
    # sess = misc.get_default_session()
    a, d, dx = get_androguard_obj(file_path)
    # a,d,dx = misc.AnalyzeAPK(file_path,session=sess)
    # way1:从字符串角度入手
    # 获取smali中的所有string
    strs = dx.get_strings()
    print("get strings finish")
    # 获取资源文件中的string
    str_arsc_id = output_arsc_strings(a)
    print("get arsc strings finish")
    # session.Save(sess,"androguard_session.ag")
    # 使用Textblob处理英文字符。使用Snownlp处理中文语句情感
    output_calling_method_neg(strs)

    # 搜索str_arsc中的内容,每一行都是一个十进制id

    # 基本思路：匹配以smali为后缀的文件，在其中搜索对nameid的使用

    # 使用chdir进入apktool工作目录
    os.chdir(work_file_path)

    # 使用apktool 对apk文件进行反编译得到smali文件 输出文件名：smali_out
    os.system("apktool d -f -r -o smali_out "+file_path)

    # 如果文件里出现中文乱码，修改file encode为GB1213  参考：https://blog.csdn.net/ixusy88/article/details/106391247

    # 使用echo 重置或创建result.txt文件
    os.system("echo asrc string search result: >result.txt")

    for s in str_arsc_id:
        s_dec = int(s, 10)
        s_hex = hex(s_dec)
        serach_str = str(s_hex)

        # 使用echo向文件中输入分割线与提示内容
        os.system("echo ------separationline---------- >> result.txt")
        os.system("echo search string: "+serach_str+" >> result.txt")
        os.system("echo search result: >> result.txt")

        # 使用findstr命令递归搜索当前目录及其子目录下的所有smali文件，并追加到result.txt文件中
        # findstr 相关参数与介绍 参考：https://www.netingcn.com/window-findstr-command.html

        os.system("findstr /MSI \""+serach_str+"\" *.smali >> result.txt")
        os.system("echo ------separationline---------- >> result.txt")

    print("语义分析完成")
