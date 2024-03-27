启动GPU镜像：

`docker run --hostname=TorchDev --gpus all -it --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 --network=host --volume=D:\Workspace:/root/workspace:rw  nvcr.io/nvidia/pytorch:24.02-py3`

清华源：
```
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-security main restricted universe multiverse
```
