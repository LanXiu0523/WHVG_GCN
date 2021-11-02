## SDtoHVG目录的作用是将时间序列转化为水平可视图(HVG)



### 数据样本选取：

**数据来源：**[Download a Data File | Case School of Engineering | Case Western Reserve University](https://engineering.case.edu/bearingdatacenter/download-data-file)

![NormalData.jpg](https://i.loli.net/2021/11/01/VAhNXTj4nJEoGDr.jpg)



![FaultData.jpg](https://i.loli.net/2021/11/01/tqvoyjNgexk8m5p.jpg)



**对应的本地数据：**

![LocalData.jpg](https://i.loli.net/2021/11/01/vMR6CrgPfVpsDyi.jpg)





### 生成的HVG数据存储格式：

```Bash
>>>This 1st section of the load_data function reads every row in the text file.
>>>The first row of every graph will provide you with 2 things, the number of nodes, the associated label
>>>The subsequent rows represent each node, and will begin with 0
>>>Represented in this order  (0,number of connections, <nodes that they are connected to>)
```



### Tips：

**该功能的实现语言为Python，对大容量数据样本的处理时间不够理想，采用C/C++等语言实现将会大大提升处理效率。**