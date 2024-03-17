# Why `code_assistant`

1. Code目标明确，有明确的可测试和衡量标准
2. Python运行环境 (nbclient、ipykernel) 成熟
3. 可以作为其他重复性较高任务的辅助编码工具

# HowTo

* 避免具体任务编排，由GPT自己拆解和规划任务
* 提供成功案例 (few shot) 作为执行参考（可附加成功的cases）
* 通过生成代码来调用具体工具 (如抓取)，运行失败则反馈并再次规划
* 中间插入人类Review环节，可用人工提示提升成功率

# TODO

Plan-and-execute方案（或Plan-and-action）

- [ ] 用户任务拆解，生成DAG的tasks列表 -> tasks
- [ ] 选取当前task，生成解决任务的代码（可能需要继续拆解？） -> str(stdout)
- [ ] CodeReview代码，检查输入输出以及执行约束条件
- [ ] 准备nb环境，运行生成的代码，获取stdout
- [ ] Code和执行结果附加，检查当前任务是否完成
- [ ] 如果任务无法完成，重新调整规划并附上无法完成原因