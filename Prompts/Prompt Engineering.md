- Prompt engineering
    
    - GPT best practices
        
        - Write clear instructions
            
            - 在输入中包含详细信息以获取更相关的答案
                
            - 要求模型模仿角色
                
            - 使用分隔符清楚地隔开输入的不同部分
                
            - 指定完成任务所需的步骤
                
            - 提供示例
                
            - 指定所需的输出长度
		
        - Provide reference text
            
            - 指示模型使用参考文本回答
                
            - 指示模型使用参考文本中的引用进行回答
		
        - Split complex tasks into simpler subtasks
            
            - 使用意向分类确定与用户查询最相关的说明
                
                - 输出非结构化的检查流程
                    
            - 对于需要很长对话的对话应用程序，请汇总或筛选以前的对话
                
                - Read this section, recapitulate the content of this section with less than 2048 words: {CONTENT 1~N}
                
                - Extract the main idea of this section.
                    
                    - The main idea of the previous section is? {每轮总结的输出结果}
                        
            - 分段汇总长文档，递归构建完整摘要
                
                - Recursively Summarizing Books with Human Feedback
		
        - Give GPTs time to "think"
            
            - 指示模型在匆忙得出结论之前制定自己的解决方案
                
            - 使用内心独白或一系列查询来隐藏模型的推理过程
                
                - 上面例子的补充：对于某些应用程序，模型用于得出最终答案的推理过程不适合与用户共享。例如，在辅导申请中，我们可能希望鼓励学生制定自己的答案，但模型对学生解决方案的推理过程可能会向学生揭示答案
                    
                - 多步方案，不会因考虑用户方案造成偏差
                    
                    - 要求GPT先自己解决问题
                        
                    - 让模型使用所有可用信息来评估学生解决方案的正确性
                        
                    - 让模型使用自己的分析来构建一个有用的导师的角色
                        
            - 询问模型在以前的传递中是否遗漏了任何内容
		
        - Use external tools
            
            - 使用基于嵌入的搜索实现高效的知识检索
                
                - langchain
                    
                - minichain
                    
            - 使用代码执行执行更准确的计算或调用外部 API
                
                - Function calling and APIs
                    
                    - 利用GPT的语言理解能力
		
        - Test changes systematically
            
            - 科学评估需要更大的评估(evals)样本量
                
            - 评估可以由人或GPT来完成
                
                - https://github.com/openai/evals
                    
                - 偏向于感性的评估，可以参考Meta LIMA里的GSB评估方法
                    
            - 参考黄金标准答案评估模型输出
                
                - gold-standard answers
                    
                - 要求输出符合要求的事实数量，而不是直接得出答案
                    
                - 也可以转换问题为分类问题，让GPT给出评判
		
        - Other resources
            
            - OpenAI cookbook
        
    - 思维提示链类
        
        - Chain-of-Thoughts
            ![[CoT.png]]
            - Using few-shot prompts to ask models to think step by step improves their reasoning
                
                - PaLM's score on math word problems (GSM8K) rises from 18% to 57%
                    
            - 原始论文
                
                - 通过思维提示链提升大语言模型的arithmetic, commonsense, symbolic reasoning tasks方面能力
                    
                - 模型规模方案与2个旧方案介绍
                    
                    - 增加模型规模，可提升模型性能和样本利用效率
                        
                        - Scaling laws for neural language models. arXiv:2001.08361
                            
                        - Language models are few-shot learners. NeurIPS
                            
                        - 局限性：单独增加模型规模，无法提升上述3种方面的能力
                            
                    - 之前就有通过重头训练或微调，来生成算术运算种自然语言的中间步骤；也有通过形式化符号来尝试的
                        
                - Chain-of-Thoughts
                    
                    - 通过生成自然语言的推理逻辑，能为算术计算提供助益
                        
                        - techniques for arithmetic reasoning can benefit from generating natural language rationales that lead to the final answer
                            
                    - 大语言模型通过prompting，表现出非常好的few shot学习能力
                        
                        - Language models are few-shot learners. NeurIPS
                            
                        - 核心：input, chain of thought, output
                            
                        - 提供一些few shot示例参考
                            
                - 关键信息
                    
                    - 提升模型规模至关重要，7B基本没区别
                        
                    - 消融研究 (Ablation Study)
                        
                        - 仅提供公式，对推理过程没有助益
                            
                        - 让模型不输出中间推理，直接输出 (...) 也是有效的
                            
                            - 说明提升能力的不是中间输出的推理内容，而是思维提升过程
                                
                        - 思维链输出在答案之后，不会影响推理效果
                            
                    - 不同的提示词组织方式，对CoT的影响较小
                        
                        - 思维链本身的提升，并不依赖于语言组织风格
                            
        - Self-Consistency CoT
            ![[Self-Consistency_CoT.png]]
            - https://zhuanlan.zhihu.com/p/609739922
                
        - Explicit CoT
            ![[Explicit CoT.png]]
        - Active Prompting CoT
            ![[Active Prompting CoT.png]]
            - 评估CoT的方法
                
        - Multimodal CoT
            ![[Multimodal CoT.png]]
    - 归纳总结类
        
        - Tree of Thoughts
            ![[Tree of Thoughts.png]]
        - 头脑风暴提示
            ![[头脑风暴提示.png]]
        - Progressive-Hint
            ![[Progressive-Hint.png]]
            - https://github.com/chuanyang-Zheng/Progressive-Hint
                
        - Plan-and-Solve
            ![[Plan-and-Solve.png]]
            - https://github.com/AGI-Edgerunners/Plan-and-Solve-Prompting

案例：[[Claude Prompt Helper]]