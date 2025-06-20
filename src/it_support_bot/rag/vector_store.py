from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Carga los documentos desde el txt
def load_documents():
    loader = TextLoader("src/it_support_bot/rag/documents/faqs.txt")
    documents = loader.load()
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(documents)

# Crea o carga el vector store con Chroma
def get_vector_store():
    docs = load_documents()
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory="src/it_support_bot/rag/chroma_db"
    )
    vectordb.persist()
    return vectordb

# Función de consulta RAG para responder preguntas
def ask_question(question: str) -> str:
    vectordb = get_vector_store()
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )
    return qa_chain.run(question)
