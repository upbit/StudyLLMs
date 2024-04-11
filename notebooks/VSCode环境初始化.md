## 镜像安装

选取GPU镜像，最好带CUDA驱动。nvidia-smi 查看驱动版本：
```
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.161.07             Driver Version: 535.161.07   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
```

如果太老则去 [https://developer.nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads) 安装新版驱动。
版本比较新就不需要升级，接着装cuDNN: https://developer.nvidia.com/rdp/cudnn-archive
解压缩并复制到 **/usr/local/cuda-12.x**，查看cuDNN版本，这里对应的也就说8.9.6.x：
```bash
$ cat /usr/local/cuda/include/cudnn_version.h | grep CUDNN_MAJOR -A 2
#define CUDNN_MAJOR 8
#define CUDNN_MINOR 9
#define CUDNN_PATCHLEVEL 6
--
#define CUDNN_VERSION (CUDNN_MAJOR * 1000 + CUDNN_MINOR * 100 + CUDNN_PATCHLEVEL)
```

## 准备gpu docker环境

参考 https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html 配置GPU docker环境。

如果是Windows宿主机，可能还要映射 /var/run/docker.sock 到内部，参考：
https://stackoverflow.com/questions/36765138/bind-to-docker-socket-on-windows


## 配置VSCode环境

修改shell为zsh：[terminal-shells](https://code.visualstudio.com/docs/terminal/basics#_terminal-shells)

VSCode用户配置参考：
```json
{
	"terminal.integrated.defaultProfile.linux": "zsh",
    "workbench.sideBar.location": "right",
    "workbench.iconTheme": "vscode-icons",
    "editor.minimap.renderCharacters": false,
    "editor.minimap.enabled": true,
    "editor.rulers": [
      80,
      120
    ],
    "files.eol": "\n",

    "go.useLanguageServer": true,
    "[go]": {
      "editor.snippetSuggestions": "none",
      "editor.formatOnSave": true,
      "editor.codeActionsOnSave": {
        "source.organizeImports": "explicit"
      }
    },
    "gopls": {
      "completeUnimported": true,
      "usePlaceholders": true,
      "completionDocumentation": true,
      "hoverKind": "SynopsisDocumentation"
    },
    "go.coverOnSave": false,
    "go.coverageDecorator": {
      "type": "gutter",
      "coveredHighlightColor": "rgba(64,128,128,0.5)",
      "uncoveredHighlightColor": "rgba(128,64,64,0.25)",
      "coveredGutterStyle": "blockgreen",
      "uncoveredGutterStyle": "blockred"
    },
    "go.coverOnSingleTest": true,
    "go.autocompleteUnimportedPackages": true,
    "go.gocodePackageLookupMode": "go",
    "go.gotoSymbol.includeImports": true,
    "go.useCodeSnippetsOnFunctionSuggest": true,
    "go.useCodeSnippetsOnFunctionSuggestWithoutType": true,
    "go.docsTool": "gogetdoc",
    "go.formatFlags": [
      "-s"
    ],
    "go.testFlags": [
      "-gcflags=all=-l"
    ],

    "[python]": {
      "editor.defaultFormatter": "ms-python.black-formatter",
      "editor.formatOnSave": true
    },

    "todohighlight.keywords": [
      {
        "text": "TODO(deryzhou):",
        "color": "#fff",
        "backgroundColor": "#ffbd2a",
        "overviewRulerColor": "rgba(255,189,42,0.8)"
      },
      {
        "text": "FIXME(deryzhou):",
        "color": "#fff",
        "backgroundColor": "#f06292",
        "overviewRulerColor": "rgba(240,98,146,0.8)"
      }
    ]
  }
```

### 配置zsh

安装 https://ohmyz.sh/
```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

接着配置个人比较喜欢的 [pure 主题](https://github.com/sindresorhus/pure)
![pure](https://raw.githubusercontent.com/sindresorhus/pure/main/screenshot.png)
```bash
mkdir -p "$HOME/.zsh" && git clone https://github.com/sindresorhus/pure.git "$HOME/.zsh/pure"

# .zshrc
fpath+=($HOME/.zsh/pure)
autoload -U promptinit; promptinit
prompt pure
```

### 配置git

log树： https://stackoverflow.com/questions/1838873/visualizing-branch-topology-in-git
```bash
# ~/.gitconfig
[alias]
    gl = lg1
    lg1 = lg1-specific --all
    lg2 = lg2-specific --all
    lg3 = lg3-specific --all

    lg1-specific = log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(auto)%d%C(reset)'
    lg2-specific = log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset)%C(auto)%d%C(reset)%n''          %C(white)%s%C(reset) %C(dim white)- %an%C(reset)'
    lg3-specific = log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset) %C(bold cyan)(committed: %cD)%C(reset) %C(auto)%d%C(reset)%n''          %C(white)%s%C(reset)%n''          %C(dim white)- %an <%ae> %C(reset) %C(dim white)(committer: %cn <%ce>)%C(reset)'
```
