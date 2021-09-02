# SearchString 说明文档

## 1.概要

直接利用androguard搜素到的字符串，使用TextBlob包，对找到的字符串进行情感分析，并且输出找到的字符对应的引用位置。

## 2.get_androguard_obj(apkfile):

实现对apk的解析



## 3.textblob

TextBlob 是一个用于处理文本数据的 Python（2 和 3）库。 它提供了一个简单的 API，用于深入研究常见的自然语言处理 (NLP) 任务，例如词性标注、名词短语提取、情感分析、分类、翻译等。

这里使用textblob进行对输出的字符串进行情感分析。

快速指南：https://textblob.readthedocs.io/en/latest/quickstart.html#quickstart

