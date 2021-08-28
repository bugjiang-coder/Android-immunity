# 说明

本文件为运行OpenAndSearch.py以及OpenAndSearch_read.py文件的输出结果示例，输出的是常见弹窗API在smali代码下的路径以及弹窗方法

## OpenAndSearch.py

```smali

D:\文件\学习\课程\曦源项目\com.eg.android.AlipayGphone\支付宝_10.2.20.7000_390_com.eg.android.AlipayGphone_main_standalone\smali0\smali\android\support\multidex\MultiDexExtractor.smali
    .catch Ljava/lang/Error; {:try_start_0 .. :try_end_0} :catch_3
    .catch Ljava/lang/Error; {:try_start_1 .. :try_end_1} :catch_4
    .catch Ljava/lang/Error; {:try_start_2 .. :try_end_2} :catch_3
    const-string v9, "performExtractionsError"

D:\文件\学习\课程\曦源项目\com.eg.android.AlipayGphone\支付宝_10.2.20.7000_390_com.eg.android.AlipayGphone_main_standalone\smali0\smali\android\support\v4\content\EditorCompatGingerbread.smali
    .catch Ljava/lang/AbstractMethodError; {:try_start_0 .. :try_end_0} :catch_0

D:\文件\学习\课程\曦源项目\com.eg.android.AlipayGphone\支付宝_10.2.20.7000_390_com.eg.android.AlipayGphone_main_standalone\smali0\smali\android\support\v4\content\ModernAsyncTask$4.smali
    .catch Ljava/lang/NoSuchFieldError; {:try_start_0 .. :try_end_0} :catch_1
    .catch Ljava/lang/NoSuchFieldError; {:try_start_1 .. :try_end_1} :catch_0
```



## OpenAndSearch_read.py

该文件主要是为了方便阅读代码做了一定的调整

1. 只保留相对路径
2. 同时输出对应的行号

```smali

\smali\android\support\multidex\MultiDexExtractor.smali
[233]    .catch Ljava/lang/Error; {:try_start_0 .. :try_end_0} :catch_3
[300]    .catch Ljava/lang/Error; {:try_start_1 .. :try_end_1} :catch_4
[380]    .catch Ljava/lang/Error; {:try_start_2 .. :try_end_2} :catch_3
[3383]    const-string v9, "performExtractionsError"

\smali\android\support\v4\content\EditorCompatGingerbread.smali
[32]    .catch Ljava/lang/AbstractMethodError; {:try_start_0 .. :try_end_0} :catch_0

\smali\android\support\v4\content\ModernAsyncTask$4.smali
[44]    .catch Ljava/lang/NoSuchFieldError; {:try_start_0 .. :try_end_0} :catch_1
[60]    .catch Ljava/lang/NoSuchFieldError; {:try_start_1 .. :try_end_1} :catch_0

```

