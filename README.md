# 在家动 · 甜美陪练

一个在家使用的中文语音训练助手：用哑铃、弹力绳完成肩背训练，搭配低冲击心肺循环，并由甜美鼓励型声音介绍动作、报数和提醒休息。

**当前版本：电脑本地网页 + 可下载训练录音。** 已有语音无需显卡或付费 TTS；需要生成新文案时，再启用可选的本地 Qwen3-TTS 工作台。仓库不包含模型权重。

## 已实现

- 默认 **32 分 31 秒**完整跟练，含热身、动作介绍、换边、组间休息、心肺与放松。
- 72 条预生成中文语音，包括 1～30 报数；调整已有动作的次数、组数和节奏时，直接复用素材。
- 开始、暂停、继续、跳过和重置；实时显示动作、剩余时间与下一环节。
- 修改训练参数后同步重建时间线；准备时长会随录音长度变化，防止介绍与报数重叠。
- 下载默认方案 MP3（约 3.9 MiB）；在浏览器导出当前方案 WAV；备份与导入计划 JSON。
- 浏览器本地保存设置、静态资源离线缓存、手机宽度布局。
- 可选本地声音工作台，支持「甜美鼓励型」和「温柔知心大姐姐」。完整训练包目前采用甜美声音。

## 默认训练安排

| 环节 | 内容 | 默认安排 |
| --- | --- | --- |
| 热身 | 原地走、轻柔转肩、胸椎转动 | 5 分钟 |
| 背部 | 单臂哑铃划船 | 每侧 10 次 × 2 组，扶稳固桌面，避免扭腰 |
| 肩背 | 弹力绳面拉 | 12 次 × 2 组，轻阻力，不耸肩，检查固定点 |
| 肩部 | 哑铃侧平举 | 10 次 × 2 组，轻微屈肘，抬到舒服高度 |
| 活动控制 | 靠墙滑手 | 8 次 × 1 组，不强迫贴墙，不塌腰换高度 |
| 心肺 | 原地快走、侧向迈步、徒手轻松空击拳 | 8 分钟；每分钟活动 40 秒、慢走 20 秒 |
| 放松 | 慢走、左右轻柔胸前拉伸、放松呼吸 | 3 分钟 |

力量动作每次 4 秒，组间及换侧休息 60 秒。最后一次完成后才进入休息；总时长还包含动作讲解与准备。

这是一般居家运动安排，不能保证纠正圆肩或驼背。使用能稳定控制的重量；出现疼痛、麻木或明显不适时停止。

## 快速开始：只跟练，不安装 AI 模型

只需 Python 3，打开终端，进入仓库根目录：

```powershell
python -m http.server 4173 --bind 127.0.0.1 --directory trainer
```

浏览器打开 [http://127.0.0.1:4173/](http://127.0.0.1:4173/)，点击开始即可。关闭终端或按 `Ctrl+C` 停止。若电脑已有完整版服务占用 4173，请直接使用已运行的页面，或改用 4174。

静态模式可以跟练、设置计划和导出音频；页面中的「声音工作台」需要下方完整版服务。也可直接播放 `trainer/full-sweet.mp3`。

> 如果系统使用 Windows Python Launcher，可以把命令开头的 `python` 换成 `py -3.12`。

## 可选：安装本地声音工作台

已验证环境：Windows、Python 3.12、RTX 3060 Ti 8 GB、PyTorch 2.8.0 + CUDA 12.6。显卡仅用于生成新语音，平时跟练不需要显卡。其他硬件组合尚未验证。

### 1. 把仓库放在空间充足的盘

例如 `E:\AI\HomeTrainer-TTS`。下列命令均在仓库根目录运行。缓存、临时文件和模型路径都相对于项目目录；首次安装与下载需要联网。不要把完整环境上传 GitHub。

```powershell
. .\env.ps1
New-Item -ItemType Directory -Force tmp,cache,models,results,logs | Out-Null
py -3.12 -m venv venv
.\venv\Scripts\python.exe -m pip install torch==2.8.0+cu126 torchaudio==2.8.0+cu126 --index-url https://download.pytorch.org/whl/cu126
.\venv\Scripts\python.exe -m pip install -r requirements.txt -c constraints.txt
```

`requirements.txt` 列出直接依赖，`constraints.txt` 固定关键版本。`requirements-lock.txt` 是制作本版时的完整环境快照，已去除本机 wheel 路径；其中 CUDA 版本的 torch 仍需上述专用索引。无需安装 FlashAttention；本版采用 SDPA。

模型目录约 2.4 GiB；Python、CUDA 运行库及下载缓存还会占用数 GiB，建议预留约 15 GiB。仓库本身只保留源码、参考音色、小段 WAV 与默认 MP3。

### 2. 下载模型

```powershell
.\venv\Scripts\python.exe download_model.py
```

下载官方 `Qwen/Qwen3-TTS-12Hz-0.6B-Base` 到 `models/Qwen3-TTS-12Hz-0.6B-Base`。脚本固定本版验证的模型修订，缓存留在当前项目目录。推理服务设为离线加载。

### 3. 启动

双击 **打开训练助手.cmd**，或执行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\start_trainer.ps1
```

- 跟练页：http://127.0.0.1:4173/
- 声音工作台：http://127.0.0.1:4173/voice/
- 状态检查：http://127.0.0.1:4173/api/status

保持启动窗口开启。结束时运行 **停止训练助手.cmd**。日志在 `logs/`，新生成录音在 `results/`。工作台每次最多输入 240 字；首次生成加载模型，点击「释放显存」可卸载。

本版测试中，约 14 秒的语音生成用时约 35 秒，PyTorch 显存保留峰值约 3.2 GiB；这不是整台电脑的总显存占用，也不是实时生成保证。

## 修改文案与重新制作

1. 修改 `trainer/phrases.json`，保持已有键名与训练时间线一致。
2. 启动完整版服务，再生成缺失或文字变化的语音：

```powershell
. .\env.ps1
.\venv\Scripts\python.exe generate_sweet_bank.py
```

默认连接 `http://127.0.0.1:4173/voice`；可用 `--studio-url` 指定独立工作台，例如 `http://127.0.0.1:7861`。

3. 安装 Node.js（建议 22 LTS）后，重新检查时间线、打包语音并制作整段录音：

```powershell
.\venv\Scripts\python.exe build_sweet_release.py
```

脚本会验证录音与文字摘要，更新 `audio-bank.js`、时长元数据和默认时间线，生成完整 WAV/MP3、`trainer/offline.html` 和离线 ZIP。整段 WAV 约 89 MiB，ZIP 与单文件网页是衍生文件，默认不提交。

仅修改次数、组数、节奏和心肺时长时，直接在网页设置中操作，无需重新生成语音。

## 声音来源与技术路线

两种声音先用官方 Qwen3-TTS VoiceDesign 演示按文字描述合成参考音色，再用本地 0.6B Base 模型基于参考音频生成训练提示。属于**预训练模型推理与参考音色复用**，本项目未微调或重新训练模型。

参考音频及描述见 `reference/`；合成素材与文案对应关系见 `trainer/voice-manifest.json`。两种都是设计的合成成年女性音色，不对应指定真人；「ENFP」仅用于描述陪练风格。

上游项目：[Qwen3-TTS 官方源码](https://github.com/QwenLM/Qwen3-TTS)、[0.6B Base 模型](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base)、[音色设计演示](https://huggingface.co/spaces/Qwen/Qwen3-TTS)。上游源码和该模型标注 Apache-2.0；其授权不自动覆盖本仓库原创代码与音频，详见 [第三方说明](THIRD_PARTY_NOTICES.md)。

## 手机、离线与数据

- 实时跟练页进入后台会自动暂停，避免浏览器后台计时不可靠。需要关屏跟练时，将默认 MP3 或导出的 WAV 传到 iPhone，用音频播放器播放。
- `127.0.0.1` 只指向当前设备，不能用作手机访问电脑的地址。服务默认只监听本机，尚未制作原生 iOS App 或微信小程序。
- 本版检查了手机宽度布局，尚未做 iPhone 真机测试。后续可在现有网页基础上改进 PWA 或封装 App。
- 跟练设置保存在当前浏览器，不上传云端；本地 TTS 输出、文案记录与临时文件留在项目目录。首次下载依赖和模型需要联网。
- 为默认方案缓存语音后，跟练无需调用云端 TTS。切换设备或浏览器不会自动同步设置。

## 目录

```text
trainer/                  网页、时间线引擎、72 条语音、默认 MP3
  tools/test-core.cjs     时间线自动检查
reference/                两种合成参考音色与文字描述
local_studio.py           本地 Qwen TTS 工作台
training_server.py        FastAPI 静态网页与 Gradio 集成入口
start_trainer.ps1         Windows 启动与状态检查
generate_sweet_bank.py    生成变更语音，复用已有缓存
build_sweet_release.py    语音打包、时间线验证、录音与离线包制作
download_model.py         可选模型下载
models/ venv/ cache/      本地模型、环境、缓存（不提交）
results/ tmp/ logs/       生成结果、临时文件、日志（不提交）
```

## 验证与已知限制

```powershell
node trainer/tools/test-core.cjs
```

已通过 85 组时间线检查：默认安排、左右侧对称、心肺分钟数、次数与节奏边界、根据录音长度调整准备时间、全程语音无重叠。已在浏览器检查开始/暂停、换边休息、设置更新与手机宽度布局；默认 MP3 已解码核对时长。

自动检查验证时间安排，不能评价动作姿势或代替对语音的听感检查。现场跟练受浏览器音频策略影响；首次点击开始时才允许播放。新语音可能有读音或音色波动，请试听后再用于训练。

## 仓库范围与授权

此仓库用于私人项目备份与继续开发，包含运行所需的静态语音素材；不包含模型、虚拟环境、下载包、缓存或个人训练历史。当前未授予原创代码与素材的额外公开使用许可；上游依赖分别遵循各自许可证。
