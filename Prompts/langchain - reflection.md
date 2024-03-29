notebook：[examples/reflexion/reflexion.ipynb](https://github.com/langchain-ai/langgraph/blob/main/examples/reflexion/reflexion.ipynb)
Reflection从原理上是可行的，核心理念：
大模型一次输出好的结果，等于要求“一口气不修改的写出好文章”；而我们人类会更多是写好后反复调整和优化：
![Reflection](https://raw.githubusercontent.com/langchain-ai/langgraph/15908adcd022c382998f57bc5f3ccc43f7f4ed05/examples/reflexion/img/reflexion.png)

在这个框架下，还有个核心是Tools的组合使用：[examples/lats/lats.ipynb](https://github.com/langchain-ai/langgraph/blob/main/examples/lats/lats.ipynb)
![Lats](https://raw.githubusercontent.com/langchain-ai/langgraph/15908adcd022c382998f57bc5f3ccc43f7f4ed05/examples/lats/img/lats.png)

和输出预测类似，Act/Tool 的使用也可以不断规划，寻找最佳的组合/执行链路，从而更好的解决问题。Langgraph里抽象为Tree Search