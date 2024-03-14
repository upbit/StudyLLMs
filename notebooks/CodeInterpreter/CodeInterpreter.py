import os
import sys
import queue
import logging
from pprint import pprint
from typing import Dict
from enum import Enum
from subprocess import PIPE
from jupyter_client import KernelManager

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class KernelState(Enum):
    "Kernel的状态定义"
    UNKNOWN = "unknown"
    READY = "ready"
    BUSY = "busy"
    IDLE = "idle"


class IOMsgType(Enum):
    "IO消息类型定义"
    UNKNOWN = "unknown"
    STREAM_STDOUT = "stream-stdout"
    STREAM_STDERR = "stream-stderr"
    STATUS = "status"


class CodeInterpreter:
    "代码解析器"
    SYSTEM_MESSAGE = """你是一位智能AI助手，你连接着一台电脑，但请注意不能联网。你可以通过使用Python来解决任务，约束条件如下：

1. 在使用Python解决任务时，你可以运行代码并得到结果，如果运行结果有错误，你需要尽可能对代码进行改进
2. 你可以处理用户上传到电脑上的文件，文件默认存储路径是/mnt/data/
""".strip()

    state = KernelState.UNKNOWN  # Kernel状态
    stdout_buffer = []  # 保存未读取的stdout消息
    stderr_buffer = []  # 保存未读取的stderr消息

    def __init__(self):
        # jupyter kernel
        self.kernel_manager = KernelManager(
            kernel_name=os.environ.get("IPYKERNEL", "python3")
        )
        self.kernel_manager.start_kernel(stdout=PIPE, stderr=PIPE)

        logging.debug(self.kernel_manager.get_connection_info())

        self.kernel = self.kernel_manager.blocking_client()
        self.kernel.start_channels()

        # Ensure the client is connected
        self.kernel.wait_for_ready()
        self.state = KernelState.READY
        logging.info("Code Interpreter started")

    def Stop(self):
        self.kernel.stop_channels()
        self.kernel_manager.shutdown_kernel()
        self.state = KernelState.UNKNOWN
        logging.info("Code Interpreter stoped")

    def RunCommand(self, code: str) -> (str, str):
        hasOut, hasErr = self.execute(code)
        return self.get_outputs(hasOut, hasErr)

    def execute(self, code: str) -> (bool, bool):
        hasOut, hasErr = False, False
        self.kernel.execute(code, silent=True)
        while True:
            try:
                io_msg = self.kernel.get_iopub_msg(timeout=1)
                match self.dispatch_message(io_msg):
                    case IOMsgType.STREAM_STDOUT:
                        hasOut = True
                    case IOMsgType.STREAM_STDERR:
                        hasErr = True
                    case IOMsgType.STATUS:
                        if self.state == KernelState.IDLE:
                            break
                    case _:
                        raise Exception("Unexpected message type")
            except queue.Empty:
                break
        return hasOut, hasErr

    def dispatch_message(self, io_msg: Dict) -> IOMsgType:
        "分发并处理消息"
        match io_msg["msg_type"]:
            case "stream":
                stream_name = io_msg["content"]["name"]
                data = io_msg["content"]["text"]
                logging.info(f"[{stream_name}]: {data}")

                if stream_name == "stdout":
                    self.stdout_buffer.append(data)
                    return IOMsgType.STREAM_STDOUT
                elif stream_name == "stderr":
                    self.stderr_buffer.append(data)
                    return IOMsgType.STREAM_STDERR

                logging.error("Unknown stream message: %s" % io_msg["content"])

            case "status":
                execution_state = io_msg["content"]["execution_state"]
                logging.debug(f"KernelState: {execution_state}")
                if execution_state == "busy":
                    self.state = KernelState.BUSY
                    return IOMsgType.STATUS
                elif execution_state == "idle":
                    self.state = KernelState.IDLE
                    return IOMsgType.STATUS

                logging.error("Unknown statue message: %s" % io_msg["content"])

            case _:
                logging.error("Unknown message type: %s" % io_msg["msg_type"])
                pprint(io_msg)

        return IOMsgType.UNKNOWN

    def get_outputs(self, hasOut: bool, hasErr: bool) -> (str, str):
        stdout, stderr = "", ""
        if hasOut:
            stdout = "".join(self.stdout_buffer)
            self.stdout_buffer.clear()
        if hasErr:
            stderr = "".join(self.stderr_buffer)
            self.stderr_buffer.clear()
        return stdout, stderr


def main():
    interpreter = CodeInterpreter()

    stdout, stderr = interpreter.RunCommand(
        """import json, pprint

pprint.pprint(json.dumps({"data": [1, 2, 3, 4, 5]}))
"""
    )
    print(stdout)
    print(stderr)

    interpreter.Stop()


if __name__ == "__main__":
    main()
