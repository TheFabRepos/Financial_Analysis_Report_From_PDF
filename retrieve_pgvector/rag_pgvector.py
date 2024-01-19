import os
from typing import Any, List, Dict
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain.chains import ConversationalRetrievalChain
from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import PromptTemplate



EMBEDDING_MODEL = "textembedding-gecko@latest"


class PG_Vector_RAG:
    def __init__(self, collection_name):
        connection_string_pgvector = PGVector.connection_string_from_db_params (
                driver=os.getenv("PGVECTOR_DRIVER", "psycopg2"),
                host=os.getenv("PGVECTOR_HOST"),
                port=int(os.getenv("PGVECTOR_PORT")),
                database=os.getenv("PGVECTOR_DATABASE"),
                user=os.getenv("PGVECTOR_USER"),
                password=os.getenv("PGVECTOR_PASSWORD"),
            )
        embedding_function = VertexAIEmbeddings(model_name="EMBEDDING_MODEL")
        pgvector_search = PGVector(
                collection_name = collection_name,
                connection_string = connection_string_pgvector,
                embedding_function = embedding_function) 
        self.retriever = pgvector_search.as_retriever()

    def search(self, query):
        self.docsearch.search(query)


def run_llm(query: str, chat_history: List[Dict[str, Any]] = []) -> Any:

    prompt_template = """ You are a expert in extracting information from JSON content.
            Based on the JSON document: 
            {context}
            
            Answer the following question: 
            {question}
            
            You will never make up data, analysed if question can be answered with calculation. If calculation is needed, then detail step by step the approach and value used for the calculation. If the information cannot be found or calculated using the provided context then just say not available in context.
            Finally, always provide source for your answer.

            Helpful Answer:
            """
    
    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"], verbose=True
    )
    
    chat = ChatVertexAI(model_name="chat-bison-32k", max_output_tokens=1000, temperature=0)

    qa = ConversationalRetrievalChain.from_llm (
        llm=chat, retriever=pgvector_retrieval.retriever,return_source_documents=False, verbose=True, combine_docs_chain_kwargs={"prompt": prompt}
    )

    test = qa({"question": query, "chat_history": []})
    
    return test["answer"]