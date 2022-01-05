# 时间序列转化为水平可视性图(HVG)或可视图(VG)



### 目录及其对应功能介绍

```
./data:数据集样本存放目录。
该项目中出现的所有'/data'空文件夹需要用该目录替换，需要进行替换的'/data'空文件的目录有:[.\SDtoHVG\Cpp\SDtoHVG\SDtoHVG\data],[.\SDtoHVG\Python\data],[.\SDtoVG\data]。
```

```
./SDtoVG:用于将时间序列转化为可视图(VG)。
./SDtoHVG:用于将时间序列转化为水平可视性图(HVG)，其中有Python和C++版本，二者性能详见该目录下README文档。
```



### 生成的HVG／ＶＧ数据存储格式：

```Bash
This 1st section of the load_data function reads every row in the text file.
The first row of every graph will provide you with 2 things, the number of nodes, the associated label
The subsequent rows represent each node, and will begin with 0
Represented in this order  (0,number of connections, <nodes that they are connected to>)
```



### 数据样本选取：

**数据来源：**[Download a Data File | Case School of Engineering | Case Western Reserve University](https://engineering.case.edu/bearingdatacenter/download-data-file)

![NormalData.jpg](https://i.loli.net/2021/11/01/VAhNXTj4nJEoGDr.jpg)



![FaultData.jpg](https://i.loli.net/2021/11/01/tqvoyjNgexk8m5p.jpg)



**对应的本地数据：**

![LocalData.jpg](https://i.loli.net/2021/11/01/vMR6CrgPfVpsDyi.jpg)





### 依赖库及依赖环境的配置详见各子目录下的README文件。