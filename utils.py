# langchain 中的对话检索链
from langchain.chains import ConversationalRetrievalChain
# pdf 相关处理类
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

# 向量数据库
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

#def qa_agent(openai_api_key, memory, uploaded_file, question):
def qa_agent(memory, uploaded_file, question):
    model = ChatOpenAI(model="gpt-3.5-turbo",
                       #openai_api_key=openai_api_key,
                       max_tokens=2000)
    # 1、读取文件
    # PyPDFLoader不能从内存中读取文件，所以需要先保存到本地
    file_content = uploaded_file.read()
    temp_file_path = "temp.pdf"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file_content)
    loader = PyPDFLoader(temp_file_path)
    docs = loader.load()

    # 2、分割文件
    text_splitter = RecursiveCharacterTextSplitter(
        # 每个分割块的大小，单位是字符
        chunk_size=1000,
        # 每个分割块之间的重叠大小，比如上一块是从0-1000，
        # 下一个块就是从901-2000，重叠就是100
        chunk_overlap=100, 
        separators=["\n", "。", "！ ", "？", "，", "、", ""]
    )
    # 分割文档，得到一系列的文档
    # 返回值是列表，每个元素是一个Document对象
    texts = text_splitter.split_documents(docs) 

    # 3、开始向量嵌入
    # 创建一个OpenAIEmbeddings 对象
    embeddings_model = OpenAIEmbeddings() 
    # 创建一个向量数据库对象，并传入文档和嵌入模型
    db = FAISS.from_documents(texts, embeddings_model)
    # 创建一个向量数据库的检索器对象
    retriever = db.as_retriever() 

    # 至此，模型有了，检索器有了，记忆有了，就可以创建
    # 出 ConversationalRetrievalChain (带记忆的检索增强对话连)
    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory
    )
    # 调用 qa 对象，传入问题，返回回答，该返回值返回的是一个字典
    response = qa.invoke({"chat_history": memory, "question": question})
    # 上面输出的字典键包含：chat_history，question，answer
    # print(response)
    return response

