首先是 [tensorrtllm_backend](https://github.com/triton-inference-server/tensorrtllm_backend) 必须和TensorRT-LLM版本一致，不然build出来的engine plan是不可用的：
```bash
[TensorRT-LLM][ERROR] 6: The engine plan file is not compatible with this version of TensorRT, expecting library version 9.2.0.5 got 9.3.0.1, please rebuild.
[TensorRT-LLM][ERROR] 2: [engine.cpp::deserializeEngine::1148] Error Code 2: Internal Error (Assertion engine->deserialize(start, size, allocator, runtime) failed. )
```

9.2.0.5是 https://github.com/NVIDIA/TensorRT-LLM/blob/728cc0044bb76d1fafbcaa720c403e8de4f81906/docker/common/install_tensorrt.sh

# 编译 [tensorrtllm_backend](https://github.com/triton-inference-server/tensorrtllm_backend)

略。希望新版本已经自带了，或者用这个半成品镜像：`docker push upbit/triton_trt_llm`

# ~~准备 [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM)~~

因为我们用 tensorrtllm_backend 里的，不需要额外clone一份。

# 编译并安装 tensorrt_llm

```bash
$ cd /
$ git clone https://github.com/triton-inference-server/tensorrtllm_backend
$ cd /tensorrtllm_backend
$ git lfs install
$ git submodule update --init --recursive

$ cd /tensorrtllm_backend/tensorrt_llm
$ python3 ./scripts/build_wheel.py --trt_root="/usr/local/tensorrt"
Successfully built tensorrt_llm-0.9.0.dev2024031900-cp310-cp310-linux_x86_64.whl
$ pip3 install ./build/tensorrt_llm*.whl
```
注：如果 build_wheel 爆内存（默认并发线程数24，Link时内存消耗超过30G），可以尝试调大swap或者增加 `-jN` 来调小make的并发
注2：这步非常耗时，建议能找到的直接`pip install tensorrt_llm`得了

# TensorRT-LLM build engine

```bash
$ cd /tensorrtllm_backend/tensorrt_llm
$ cd examples/chatglm # 改成你的模型路径
$ ln -s /path/to/model/chatglm3-6b-32k chatglm3_6b_32k
$ python3 convert_checkpoint.py --model_dir chatglm3_6b_32k --outpu
t_dir chatglm3_6b_32k/cpkt/fp16/1-gpu
$ trtllm-build --checkpoint_dir chatglm3_6b_32k/cpkt/fp16/1-gpu --gemm_plugin float16 --output_dir chatglm3_6b_32k/engine/fp16/1-gpu
```
然后留意下输出，看看trtllm-build的版本是否正确：

`[TensorRT-LLM] TensorRT-LLM version: 0.9.0.dev2024031900`


