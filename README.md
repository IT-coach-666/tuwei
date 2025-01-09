# tuwei

设计一个基于文档（如 PDF 文档）的问答系统（chatbot 聊天机器人），文档篇幅可能很长

### 系统架构设计
1、pdf 内容解析、分块（基于 langchain 分块，允许 10-20% 的重叠，使得文档的上下文语义信息得到合理衔接）；针对 PDF 中的表格，可通过 OCR 技术获取表格信息

LLM 搭建（如果是针对）



### demo 示例

安装了 gradio 的虚拟环境
conda activate jy_py310

python demo.py

临时 demo：http://124.221.34.163:7860/




### 涉及图表信息的问题回答优化

