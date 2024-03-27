[LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)
![[AI Agent.png]]
#### Agents解决的问题：
* 模型本身的弱点（事实准确性、时效性）-> 检索增强
* 拓展模型能力边界（垂类知识，分段摘要或RAG提供输入） -> FuncCall+其他工具
* 满足复杂场景的任务处理需求 -> 角色扮演，组合使用

#### Prompt调优与精调
1. [如何高效构造大模型精调所需的高质量数据？「视频回放」](https://km.woa.com/articles/show/594304)
2. [【混元实操篇】大模型精调数据准备技巧硬核解读「视频回放」](https://km.woa.com/articles/show/598732)

**SFT经验：**
* 50~200条精调数据
* 基于结果评测、反馈
* 一般情况，4K优于32K