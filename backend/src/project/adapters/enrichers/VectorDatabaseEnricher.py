from project.ports.enrichers.ContextEnricher import ContextEnricher

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


class VectorDatabaseEnricher(ContextEnricher):
    def __init__(self):
        filepath = "src/project/database/texts/freerules-dnd.pdf"
        loader = PyPDFLoader(filepath)
        documento = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        splits = text_splitter.split_documents(documento)

        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=OpenAIEmbeddings(),
            persist_directory="../database/chroma_db",
            collection_name="vector_database",
        )

    def getData(self, query):
        retriever = self.vectorstore.as_retriever()
        return retriever
