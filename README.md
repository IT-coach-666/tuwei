# tuwei

设计一个基于文档（如 PDF 文档）的问答系统（chatbot 聊天机器人），文档篇幅可能很长


### demo 示例

在 demo-main.py 中设置可用的 api-key：
os.environ["OPENAI_API_KEY"] = "sk-proj-xxxxx"

安装以下相关依赖包（可基于 python 3.10 安装）

pip install -r requirements.txt

streamlit run demo-main.py

临时 demo：http://124.221.34.163:8501/



### 系统架构设计
<img width="323" alt="image" src="https://github.com/user-attachments/assets/91cef89e-1254-4c09-8740-93005f498ec2" />

#### 1、pdf 内容解析、分块

使用 PyPDF2 库（langchain_community 中封装了 PyPDFLoader 类）读取 pdf 文件（针对 PDF 中的表格，可通过 OCR 技术获取表格信息）

使用 langchain 将读取的文本切分成小段，允许 10-20% 的重叠，使得文档的上下文语义信息得到合理衔接


#### 2、将分块文本信息向量化、存入数据库

文本片段向量化、创建索引：

1）向量化可通过 openai 的 embedding 接口，将文档转化为向量；也可以训练向量化模型或使用开源模型，并部署到本地环境

2）将转化后的向量存入 Pinecone 向量数据库（也可以自己创建数据库，并基于 faiss / milvus 工具建索引，实现快速高效查询）；demo 示例中使用了 langchain_community 中封装的 faiss


#### 3、从数据库中检索 query 相关度高的内容，并投喂给 LLM 进行回答

1）对 query 进行向量化，并基于向量间的相似度（如 cosine 相似度）从数据库中查找与 query 相关的 top-K 个文本片段

2）LLM 可以采用接口式请求（如 openAI 的 gpt-3.5-turbo 接口），或者基于先进开源项目（如 LLaMA、Qwen 等；如果着重考虑中文能力，可以使用 Qwen）垂直领域进行 SFT、DPO（可适当采样 LoRA、QLoRA 以及相关技术减少显存占用），并通过 vLLM 本地部署。

3）可结合 prompt 工程，适当拟定与任务相关的 prompt，如：
prompt_template = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)



### 涉及图表信息的问题回答优化

1）引入多模态系统，进行图文理解、表格理解

2）对图表进行 OCR，抽取图表中的关键信息
