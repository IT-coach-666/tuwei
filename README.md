# tuwei

设计一个基于文档（如 PDF 文档）的问答系统（chatbot 聊天机器人），文档篇幅可能很长


### demo 示例

在 demo-main.py 中设置可用的 api-key：
os.environ["OPENAI_API_KEY"] = "sk-proj-xxxxx"

安装以下相关依赖包（可基于 python 3.10 安装）

pip install -r requirements.txt

streamlit run demo-main.py

临时 demo：http://124.221.34.163:8501/（注意：openAI 接口在网络不稳定的情况下，即使 API-key 有效，也要等待请求很久）

<img width="888" alt="image" src="https://github.com/user-attachments/assets/4d6424c3-70f5-4339-b8f8-25bf27127157" />


### 系统架构设计
<img width="323" alt="image" src="https://github.com/user-attachments/assets/91cef89e-1254-4c09-8740-93005f498ec2" />

该任务可以理解为一个 RAG 系统，实现思路说明如下。

#### 1、pdf 内容解析、分块

1）使用 PyPDF2 库（langchain_community 中封装了 PyPDFLoader 类）读取 pdf 文件（针对 PDF 中的表格，可通过 OCR 技术获取表格信息）

2）使用 langchain 将读取的文本切分成小段，允许 10-20% 的重叠，使得文档的上下文语义信息得到合理衔接

3）对于特点领域，如果存在些累赘的文本、或重复度较高的文本，可进行去重和相应的过滤操作（比如在专利领域，一篇规范化的专利文本信息中，有些信息是主要的，有些信息则是套话、千篇一律，因此可对千篇一律的内容进行过滤）


#### 2、将分块文本信息向量化、存入数据库

文本片段向量化、创建索引：

1）向量化可通过 openai 的 embedding 接口，将文档转化为向量；也可以训练向量化模型或使用开源模型，并部署到本地环境

2）将转化后的向量存入 Pinecone 向量数据库（也可以自己创建数据库，并基于 faiss / milvus 工具建索引，实现快速高效查询）；demo 示例中使用了 langchain_community 中封装的 faiss


#### 3、从数据库中检索 query 相关度高的内容，并投喂给 LLM 进行回答

1）对 query 进行向量化，并基于向量间的相似度（如 cosine 相似度）从数据库中查找与 query 相关的 top-K 个文本片段；该检索过程的返回信息如果不太满足要求，则可以基于特定任务下的数据训练专有的语义模型，对原搜索结果进行 rerank；语义模型有早期基于双塔结构进行 finetune 的（如 Sentence-Bert）、基于 pretrain 和 fintune 的 cross-encoder 架构（如 RetroMAE、BGE、BGE-M3 等）、以及基于 LLM 架构的（如 NV-embed），对应的论文可参考：https://www.yuque.com/it-coach/read-paper/zf55t7ehkq711qqf

2）LLM 可以采用接口式请求（如 openAI 的 gpt-3.5-turbo 接口），或者基于先进开源项目（如 LLaMA、Qwen 等；如果着重考虑中文能力，可以使用 Qwen）垂直领域进行 SFT、DPO（可适当采样 LoRA、QLoRA、BAdam 等相关技术减少显存占用），并通过 vLLM 本地部署。

3）可结合 prompt 工程，适当拟定与任务相关的 prompt，如：prompt_template = "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, say that you don't know. Use three sentences maximum and keep the answer concise. \n\n {context}"

4）可额外对 query 进行处理分析、query 理解，比如识别出 query 文本中的时间期限等受限条件，即可进行更精细化的检索；或者利用 LLM 对 query 进行更智能化的改写（结合特定的 prompt，让 LLM 辅助理解 query 的真实意图），以实现更精确查找（包含扩充 query 中专有名词的不同表述、同义词等）。


### 涉及图表信息的问题回答优化

1）引入多模态系统，进行图文理解、表格理解

2）对图表进行 OCR，抽取图表中的关键信息
