# SearchAPI 说明文档

## 1.概要

直接利用androguard搜素到的api

androguard GitHub地址:https://github.com/androguard/androguard





下面罗列重要函数的用法，以及使用的一些重要函数的用法



## 2.使用的重要函数

### 2.1.find_methods()：

find_methods(classname=’.\*’*,* *methodname=’.\*’,* *descriptor=’.\*’,* accessflflags=’.\*’,no_external=False)：

该函数会找到指定的方法，方法的表示使用**正则表达式**

```python
    #源码 
    def find_methods(self, classname=".*", methodname=".*", descriptor=".*",
            accessflags=".*", no_external=False):
        """
        Find a method by name using regular expression.
        This method will return all MethodAnalysis objects, which match the
        classname, methodname, descriptor and accessflags of the method.
        :param classname: regular expression for the classname
        :param methodname: regular expression for the method name
        :param descriptor: regular expression for the descriptor
        :param accessflags: regular expression for the accessflags
        :param no_external: Remove external method from the output (default False)
        :rtype: Iterator[MethodAnalysis]
        """
        classname = bytes(mutf8.MUTF8String.from_str(classname))
        methodname = bytes(mutf8.MUTF8String.from_str(methodname))
        descriptor = bytes(mutf8.MUTF8String.from_str(descriptor))
        for cname, c in self.classes.items():
            if re.match(classname, cname):
                for m in c.get_methods():
                    z = m.get_method()
                    # TODO is it even possible that an internal class has
                    # external methods? Maybe we should check for ExternalClass
                    # instead...
                    if no_external and isinstance(z, ExternalMethod):
                        continue
                    if re.match(methodname, z.get_name()) and \
                       re.match(descriptor, z.get_descriptor()) and \
                       re.match(accessflags, z.get_access_flags_string()):
                        yield m
```

https://github.com/androguard/androguard/blob/master/androguard/core/analysis/analysis.py