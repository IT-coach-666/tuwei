# tuwei

设计一个基于文档（如 PDF 文档）的问答系统（chatbot 聊天机器人），文档篇幅可能很长

### 系统架构设计
1、pdf 内容解析、分块

使用 PyPDF2 库（langchain_community 中封装了 PyPDFLoader 类）读取 pdf 文件（针对 PDF 中的表格，可通过 OCR 技术获取表格信息）

使用 langchain 将读取的文本切分成小段，允许 10-20% 的重叠，使得文档的上下文语义信息得到合理衔接


2、将分块文本信息向量化、存入数据库（如果数据量少，存入内存也可以）

通过 openai 的 embedding 接口，将文档转化为向量（也可以自己训练向量化模型或使用开源模型，并部署到本地环境）

将转化后的向量存入 Pinecone 向量数据库（也可以自己创建数据库，并基于 faiss / milvus 工具建索引，实现快速高效查询）；demo 示例中使用了 langchain_community 中封装的 faiss


3、从数据库中检索 query 相关度高的内容，并投喂给 LLM 进行回答

对 query 进行向量化，并基于向量间的相似度（如 cosine 相似度）从数据库中查找与 query 相关的 top-K 个文本片段

LLM 可以采用接口式请求，或者基于先进开源项目（如 LLaMA、Qwen 等；如果着重考虑中文能力，可以使用 Qwen）垂直领域进行 SFT、DPO（可适当采样 LoRA、QLoRA 以及相关技术减少显存占用），并通过 vLLM 本地部署。




LLM 搭建（如果是针对）



### demo 示例

在安装以下相关依赖包的虚拟环境（conda activate jy_py310）

pip install -r requirements.txt

streamlit run demo-main.py

临时 demo：http://124.221.34.163:8501/




### 涉及图表信息的问题回答优化

