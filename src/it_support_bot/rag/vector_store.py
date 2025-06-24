import os
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, UnstructuredPDFLoader
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Cargar documentos en un vector store
def load_documents():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(base_dir, "documents")
    all_documents = []
    for filename in os.listdir(docs_dir):
        file_path = os.path.join(docs_dir, filename)
        if filename.lower().endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
        elif filename.lower().endswith(".pdf"):
            loader = UnstructuredPDFLoader(file_path)
        else:
            continue  
        try:
            all_documents.extend(loader.load())
        except Exception as e:
            print(f"Error cargando {filename}: {e}")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_documents(all_documents)

# Crea un vector store usando los documentos cargados
def get_vector_store():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    persist_dir = os.path.join(base_dir, "chroma_db")
    embeddings = OpenAIEmbeddings()
    docs = load_documents()

    # Si ya existe el vector store, lo carga; si no, lo crea
    if os.path.exists(persist_dir) and os.listdir(persist_dir):
        vectordb = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
        vectordb.add_documents(docs)
    else:
        vectordb = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=persist_dir
        )
    return vectordb

# Función para hacer preguntas al vector store
def ask_question(question: str) -> str:
    vectordb = get_vector_store()
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )
    result = qa_chain.invoke({"query": question})
    return result["result"]