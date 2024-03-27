参考：[How to generate text](https://huggingface.co/blog/zh/how-to-generate)

## Temperature

这个参数大家应该都了解。从 https://www.bilibili.com/video/BV1rm411R7d9 看到个比较形象的说明，影响的是候选词概率的随机性：
![[temperature.png]]

## 主流解码方式

**贪心搜索**比较好理解，直接选下一次候选词概率最大的（但不一定是最优路径）：
![贪心搜索](https://huggingface.co/blog/assets/02_how-to-generate/greedy_search.png)

所以另一种策略是**集束搜索**(Beam Search)，会选择链路上的最大概率：
![Beam Search](https://huggingface.co/blog/assets/02_how-to-generate/beam_search.png)


## top_k

top_k 就是向后看token的个数，`=1`时代表贪心搜索，`>1`时则为集束搜索。

但留意，概率最大在文本上不一定是最佳的（缺少“惊喜”），实验发现人类优质文本的概率是波动的，和BeamSearch的背道而驰：
![Less Surprising](https://blog.fastforwardlabs.com/images/2019/05/Screen_Shot_2019_05_08_at_3_06_36_PM-1557342561886.png)

## 采样

既然直接 BeamSearch 不行，那自然考虑引入“随机性”。最极端的是`top_k=0`全随机采样：

![sampling_search](https://huggingface.co/blog/assets/02_how-to-generate/sampling_search.png)

这样导致生成的内容可能 car 后面并不一定跟着 drives。因此引入 `temperature` 的概念，来调整词的分布陡峭度，让我们抽到的词符合“规律”：

![sampling search with temp](https://huggingface.co/blog/assets/02_how-to-generate/sampling_search_with_temp.png)

注意：特殊的 `temperature=0` 就会退化回贪心搜索

## top_p

既然采样也不太行，有没有更好的策略？
GPT-2里采用了一种“在 _Top-K_ 采样中，概率最大的 _K_ 个词会被选出，然后这 _K_ 个词的概率会被重新归一化，最后就在这重新被归一化概率后的 _K_ 个词中采样”的方法：
![top_p](https://huggingface.co/blog/assets/02_how-to-generate/top_k_sampling.png)

第一步6个候选词概率为68%，到第二步就接近99%了（同时去掉了那些“不太合理”的词）

## top_p (nucleus)

上面方案候选词6个，当分布不同时可能存在问题。例如左边有些不错的候选词被剔除，而右边 (car, down) 这种很少出现的又会被纳入，所以候选词个数可能并不适合固定。

因此用“候选词的累计概率”就顺应而出，可以看到第一步候选词变多，第二步确定情况则减少候选词：
![nucleus](https://huggingface.co/blog/assets/02_how-to-generate/top_p_sampling.png)


## 结合的情况

实际情况 `top_p` 和 `top_k` 是可以一起使用的。实际情况是先进行 top_k 采样，然后从中选取归一化后符合的 top_p 的前N个候选：
![[top_k_p.png]]

OpenAI推荐的参数如下（不支持`top_k`）：[Mastering Temperature and Top_p in ChatGPT API](https://community.openai.com/t/cheat-sheet-mastering-temperature-and-top-p-in-chatgpt-api/172683)

|Use Case|Temperature|Top_p|Description|
|---|---|---|---|
|Code Generation|0.2|0.1|Generates code that adheres to established patterns and conventions. Output is more deterministic and focused. Useful for generating syntactically correct code.|
|Creative Writing|0.7|0.8|Generates creative and diverse text for storytelling. Output is more exploratory and less constrained by patterns.|
|Chatbot Responses|0.5|0.5|Generates conversational responses that balance coherence and diversity. Output is more natural and engaging.|
|Code Comment Generation|0.3|0.2|Generates code comments that are more likely to be concise and relevant. Output is more deterministic and adheres to conventions.|
|Data Analysis Scripting|0.2|0.1|Generates data analysis scripts that are more likely to be correct and efficient. Output is more deterministic and focused.|
|Exploratory Code Writing|0.6|0.7|Generates code that explores alternative solutions and creative approaches. Output is less constrained by established patterns.|
