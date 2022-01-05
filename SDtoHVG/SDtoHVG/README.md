# 时间序列转化为水平可视图(HVG)



## C++实现与Python实现的性能对比：

**对一份102400*10时间节点的数据集样本，以每个HVG含1024个时间节点的情况进行数据处理，生成1000个HVG图。Python实现耗时约6000s，C++实现耗时约为180s，可见该处理情况下C++实现的数据处理速率是Python实现的数据处理速率的33倍以上，对较大的数据样本应采用C++实现，对不追求处理速率的小样本也可以考虑采用配置更为简单的Python实现。**

<a href="https://sm.ms/image/hoQ16VkYbpmcAXw" target="_blank"><img src="https://s2.loli.net/2022/01/05/hoQ16VkYbpmcAXw.jpg" ></a>



## Python实现的运行环境与依赖环境配置

### 运行环境

```
python 3.9.6
```



### 安装依赖项

```
pip install -r requirements.txt
```



## C++实现的运行环境与依赖环境配置

### 运行环境

```
Visual Studio 2017 15.9.36
```



### 工程依赖环境配置

##### 1.由于所安装的matlab为64位，要调用其函数，需要将工程转换为X64:

```
顶菜单->生成->配置管理器->平台：X64 
```

```
VC++ 目录->链接器->高级->目标计算机:MachineX64(/MACHINE:X64)
```

##### 2.VC++ 目录->包含目录 添加: 

```
MATLAB\R2010b\extern\include  
MATLAB\R2010b\extern\include\win64  
```

##### 3.VC++ 目录->库目录 添加：

```
MATLAB\R2010b\extern\lib\win64\microsoft  
MATLAB\R2010b\extern\lib\win32\microsoft  
```

##### 4.VC++ 目录->常规->附加包含目录 添加: 

```
MATLAB\R2010b\extern\include  
MATLAB\R2010b\extern\include\win64  
```

##### 5.VC++ 目录->链接器->输入->附加依赖库 添加:

```
libmat.lib  
libmx.lib  
libmex.lib  
libeng.lib  
```

##### 6.计算机环境变量->path 添加： 

```
MATLAB\R2010b\extern\lib\win64\microsoft;  
MATLAB\R2010b\bin\win64;  
```

##### 7.顶菜单->项目->属性->连接器->系统->堆栈保留大小 的值为:[1,073,741,824]

**Tips：以上所有目录应修改为计算机上对应的绝对路径。**

