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



```python
class MethodAnalysis:
    """
    This class analyses in details a method of a class/dex file
    It is a wrapper around a :class:`EncodedMethod` and enhances it
    by using multiple :class:`DVMBasicBlock` encapsulated in a :class:`BasicBlocks` object.

    :type vm: a :class:`DalvikVMFormat` object
    :type method: a :class:`EncodedMethod` object
    """
    #下面有重要方法
    def get_method(self):
            """

            :rtype: androguard.core.bytecodes.dvm.EncodedMethod
            :return:
            """
            return self.method
```



```python
class EncodedMethod:
    """
    This class can parse an encoded_method of a dex file

    :param buff: a string which represents a Buff object of the encoded_method
    :type buff: Buff object
    :param cm: a ClassManager object
    :type cm: :class:`ClassManager`
    """
	#获取源码
    def source(self):
        """
        Return the source code of this method

        :rtype: string
        """
        self.CM.decompiler_ob.display_source(self)

    def get_source(self):
        return self.CM.decompiler_ob.get_source_method(self)
    
        def get_instructions(self):
        """
        Get the instructions

        :rtype: a generator of each :class:`Instruction` (or a cached list of instructions if you have setup instructions)
        """
        if self.get_code() is None:
            return []
        return self.get_code().get_bc().get_instructions()
```



`self.vms`来自`androguard/core/bytecodes/dvm.py`的`class DalvikVMFormat(bytecode.BuffHandle)`







```python
class Instruction:
    """
    This class represents a Dalvik instruction

    It can both handle normal instructions as well as optimized instructions.

    .. warning::
        There is not much documentation about the optimized opcodes!
        Hence, it relies on reverese engineered specification!

    More information about the instruction format can be found in the official documentation:
    https://source.android.com/devices/tech/dalvik/instruction-formats.html

    .. warning::
        Values stored in the instructions are already interpreted at this stage.

    The Dalvik VM has a eight opcodes to create constant integer values.
    There are four variants for 32bit values and four for 64bit.
    If floating point numbers are required, you have to use the conversion opcodes
    like :code:`int-to-float`, :code:`int-to-double` or the variants using :code:`long`.

    Androguard will always show the values as they are used in the opcode and also extend signs
    and shift values!
    As an example: The opcode :code:`const/high16` can be used to create constant values
    where the lower 16 bits are all zero.
    In this case, androguard will process bytecode :code:`15 00 CD AB` as beeing
    :code:`const/high16 v0, 0xABCD0000`.
    For the sign-extension, nothing is really done here, as it only affects the bit represenation
    in the virtual machine. As androguard parses the values and uses python types internally,
    we are not bound to specific size.
    """
```









## 2.dalvik虚拟机对static field的优化

对下面这句话的理解

`**Note:** Calls to static fields are usually not tracked, as they are optimized by the compiler to const calls!`





```java
class A{
    public static int e; //public static field公共静态域
    
    public void a() {
		e = 1;
		System.out.println(e);
	}
    
    public static void main(String[] args) {
		a();//调用方法a	
	}

}
```



如果静态字段`e `没有被修改，会被dalvik虚拟机优化成下面的样子

```java
class A{
   // 被优化掉 public static int e; 
    
    public void a() {
		// 被优化掉 e = 1;
		System.out.println(1);
	}
    
    public static void main(String[] args) {
		a();//调用方法a	
	}

}
```



也就是说上面的情况下，使用交叉引用去找`a`方法的调用字段，`call to`也就是`xref_to` 是不会有`e`这一个字段的，因为**被优化掉了**，这个调用被优化为了"内联函数" 。



参考：

https://stackoverflow.com/questions/11445996/will-java-compiler-optimize-a-method-call-on-a-final-static-variable-and-what/11457426  get inlined

https://www.thinbug.com/q/11445996 内联短函数



## 结论

这个note对我们的项目没有任何影响，对这个static field的调用是本身在smali代码中就被优化了的，该检索的string和method依然会被检索出来