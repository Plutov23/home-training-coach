# Third-party notices / 第三方说明

- **Qwen3-TTS**：https://github.com/QwenLM/Qwen3-TTS ，上游源码标注 Apache-2.0。
- **Qwen3-TTS-12Hz-0.6B-Base**：https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base ，模型卡标注 Apache-2.0。模型权重未收录于本仓库，按需从官方仓库下载。
- **参考音色**：由官方 Qwen VoiceDesign 演示 https://huggingface.co/spaces/Qwen/Qwen3-TTS 根据文字描述合成；提示描述、原始参考文案与文件名在 `reference/两种陪练音色设计.json`。没有指定真人身份。
- **训练语音**：基于上述合成参考音色，使用本地预训练模型生成，未做微调。WAV 片段、内嵌 JS 数据及完整 MP3 属于同一套素材的不同封装。
- **运行依赖**：PyTorch、Transformers、Gradio、FastAPI、NumPy、SoundFile、imageio-ffmpeg 等按各自发布的许可使用。此仓库仅列出依赖，不随附这些软件的二进制环境或模型。

上游 Apache-2.0 不构成本仓库所有文件的统一授权。原创代码与生成音频目前未另行指定开放许可证；公开分发或商用前应分别确认相关许可和音频来源要求。
