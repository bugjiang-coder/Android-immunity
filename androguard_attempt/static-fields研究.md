# static fields研究



在androguard的文档中有下面的一个note

> **Get XREFs for Fields**
>
> The last XREF we can use are fields. Fields are a little bit different and do not use xref_from and xref_to but
>
> xref_read() and xref_write(). You can use the method *find_methods()* in order to find fields.
>
> **Note:** Calls to static fields are usually not tracked, as they are optimized by the compiler to const calls!



为了解答或者说实现对static fields的搜索从下面两个角度入手

## 1.androguard xref的实现

位置：`androguard/core/analysis/analysis.py`

```python
 def create_xref(self):
        """
       只保留关键代码
        """
        for vm in self.vms:
            for current_class in vm.get_classes():
                self._create_xref(current_class)

        # TODO: After we collected all the information, we should add field and
        # string xrefs to each MethodAnalysis

```



```python
def _create_xref(self, current_class):
        """
只保留关键代码
        """
        cur_cls_name = current_class.get_name()

        for current_method in current_class.get_methods():
            
            cur_meth = self.get_method(current_method)
            cur_cls = self.classes[cur_cls_name]

            for off, instruction in current_method.get_instructions_idx():
                op_value = instruction.get_op_value()
#这里_create_xref通过调用vm 下 get_classes() 的 get_instructions_idx() 的 instruction 的 get_op_value()
#获得操作数，通过不同的操作数进行xref的过程
                
```







`self.vms`来自`androguard/core/bytecodes/dvm.py`的`class DalvikVMFormat(bytecode.BuffHandle)`











## 2.java对static field的优化