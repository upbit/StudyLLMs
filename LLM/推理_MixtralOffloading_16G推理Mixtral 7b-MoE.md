核心思想：2个专家模型激活，用LRU cache将常用的放在GPU，其他offloading到内存

项目：[https://github.com/dvmazur/mixtral-offloading](https://github.com/dvmazur/mixtral-offloading)
效果：[让Mixtral-8*7B模型运行在16GB显存GPU上](https://www.bilibili.com/video/BV17Q4y1A7Wp/)