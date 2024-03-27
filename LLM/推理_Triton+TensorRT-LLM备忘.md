
# 坑很多..

首先是 [tensorrtllm_backend](https://github.com/triton-inference-server/tensorrtllm_backend) 必须和TensorRT-LLM版本一致，不然build出来的engine plan是不可用的：
```bash
[TensorRT-LLM][ERROR] 6: The engine plan file is not compatible with this version of TensorRT, expecting library version 9.2.0.5 got 9.3.0.1, please rebuild.
[TensorRT-LLM][ERROR] 2: [engine.cpp::deserializeEngine::1148] Error Code 2: Internal Error (Assertion engine->deserialize(start, size, allocator, runtime) failed. )
```

但不同commit也会引发其他问题，例如 [#583](https://github.com/NVIDIA/TensorRT-LLM/issues/583)：

```
[TensorRT-LLM][ERROR] Assertion failed: d == a + length (/app/tensorrt_llm/cpp/tensorrt_llm/plugins/gemmPlugin/gemmPlugin.cpp:156)
```

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
Successfully built tensorrt_llm-0.9.0.dev2024030500-cp310-cp310-linux_x86_64.whl
$ pip3 install ./build/tensorrt_llm*.whl
```
注：如果 build_wheel 爆内存（默认并发线程数24，Link时内存消耗超过30G），可以尝试调大swap或者增加 `-jN` 来调小make的并发
注2：这步非常耗时，建议能找到的直接`pip install tensorrt_llm`得了

## undefined symbol: opal_hwloc201_hwloc_get_type_depth

缺少 hwloc-nox，相关包都重装下：
`apt purge hwloc-nox libhwloc-dev libhwloc-plugins`

# TensorRT-LLM build engine

```bash
$ cd /tensorrtllm_backend/tensorrt_llm
$ cd examples/chatglm # 改成你的模型路径
$ ln -s /path/to/model/chatglm3-6b-32k chatglm3_6b_32k
$ python3 convert_checkpoint.py --model_dir chatglm3_6b_32k --output_dir chatglm3_6b_32k/cpkt/fp16/1-gpu
$ trtllm-build --checkpoint_dir chatglm3_6b_32k/cpkt/fp16/1-gpu --gemm_plugin float16 --output_dir chatglm3_6b_32k/engine/fp16/1-gpu
```
然后留意下输出，看看trtllm-build的版本是否正确：

`[TensorRT-LLM] TensorRT-LLM version: 0.9.0.dev2024030500`

# 启动server

先准备启动配置（参考：[gemma-7b](https://github.com/GoogleCloudPlatform/kubernetes-engine-samples/blob/main/ai-ml/llm-serving-gemma/trtllm/job-download-gemma-7b.yaml)），编写如下setup.sh脚本：

```bash
MODEL_NAME="chatglm3-6b-32k"

TOKENIZER_DIR=/root/workspace/chatglm3-6b-32k
ENGINE_PATH=/root/workspace/chatglm3-6b-32k/engine/fp16/1-gpu

TRITON_MODEL_REPO=/data/triton/model_repository

# 注意gemma的tokenizer_type是sp，不是auto
python3 /tensorrtllm_backend/tools/fill_template.py -i ${TRITON_MODEL_REPO}/preprocessing/config.pbtxt tokenizer_dir:${TOKENIZER_DIR},tokenizer_type:auto,triton_max_batch_size:64,preprocessing_instance_count:1
python3 /tensorrtllm_backend/tools/fill_template.py -i ${TRITON_MODEL_REPO}/postprocessing/config.pbtxt tokenizer_dir:${TOKENIZER_DIR},tokenizer_type:auto,triton_max_batch_size:64,postprocessing_instance_count:1
python3 /tensorrtllm_backend/tools/fill_template.py -i ${TRITON_MODEL_REPO}/tensorrt_llm_bls/config.pbtxt triton_max_batch_size:64,decoupled_mode:False,bls_instance_count:1,accumulate_tokens:False
python3 /tensorrtllm_backend/tools/fill_template.py -i ${TRITON_MODEL_REPO}/ensemble/config.pbtxt triton_max_batch_size:64
python3 /tensorrtllm_backend/tools/fill_template.py -i ${TRITON_MODEL_REPO}/tensorrt_llm/config.pbtxt triton_max_batch_size:64,decoupled_mode:False,max_beam_width:1,engine_dir:${ENGINE_PATH},max_tokens_in_paged_kv_cache:2560,max_attention_window_size:2560,kv_cache_free_gpu_mem_fraction:0.5,exclude_input_in_output:True,enable_kv_cache_reuse:False,batching_strategy:inflight_batching,max_queue_delay_microseconds:600,batch_scheduler_policy:guaranteed_no_evict,enable_trt_overlap:False

echo Done!
```

然后：
```bash
$ export TRITON_MODEL_REPO=/data/triton/model_repository
$ mkdir -p ${TRITON_MODEL_REPO}
$ cd ${TRITON_MODEL_REPO}
$ cp -r /tensorrtllm_backend/all_models/inflight_batcher_llm/* ${TRITON_MODEL_REPO}
$ bash +x setup.sh

# --world_size is the number of GPUs you want to use for serving
$ python3 /tensorrtllm_backend/scripts/launch_triton_server.py --world_size=1 --model_repo=$(pwd)
```
## chatglm3-7b的can't set attribute 'pad_token'

原因：[AttributeError: can't set attribute 'eos_token' #152](https://github.com/THUDM/ChatGLM3/issues/152#issue-1975493839)

> `transformers` 的 `tokenizer` 会在 `save_pretrained` 时把 `self.special_tokens_map` 保存到 `tokenizer_config.json` 中，这就使得 `eos_token` 等冗余信息保存到了 `tokenizer_config.json`，而 ChatGLM 的 tokenizer 初始化不支持 `eos_token` 的输入

处理方式：修改前后预处理，把 `*/1/model.py` 里的 pad_token 相关行注释掉。

`# self.tokenizer.pad_token = self.tokenizer.eos_token`