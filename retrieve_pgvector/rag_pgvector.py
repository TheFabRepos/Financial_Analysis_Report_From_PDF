import os
from typing import Any, List, Dict
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import RetrievalQA
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
        embedding_function = VertexAIEmbeddings(model_name=EMBEDDING_MODEL)
        pgvector_search = PGVector(
                collection_name = collection_name,
                connection_string = connection_string_pgvector,
                embedding_function = embedding_function) 
        self.retriever = pgvector_search.as_retriever()

    def search(self, query):
        self.docsearch.search(query)


def run_llm(query: str, pgvector_retrieval:PG_Vector_RAG, chat_history: List[Dict[str, Any]] = []) -> Any:

    prompt_template = """ You are a expert in extracting information from JSON content.
            Based on the JSON document: 
            {context}
            
            Answer the following question: 
            {question}
            
            You will never make up data, try to answer with calculation if needed. If calculation is needed, think step by step and explain the approach and value used for the calculation. If the information cannot be found or calculated using the provided context then just say not available in context.

            Helpful Answer:
            """
    
    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"], verbose=True
    )
    
    #chat = ChatVertexAI(model_name="chat-bison-32k", max_output_tokens=3000, temperature=0.7)
    chat = ChatVertexAI(model_name="gemini-pro", max_output_tokens=3000, temperature=0.7)

    #qa = ConversationalRetrievalChain.from_llm (
    #    llm=chat, retriever=pgvector_retrieval.retriever,return_source_documents=True, verbose=True, combine_docs_chain_kwargs={"prompt": prompt}
    #)

    qa = RetrievalQA.from_chain_type(llm=chat, retriever=pgvector_retrieval.retriever,return_source_documents=True, verbose=True, chain_type_kwargs={"prompt": prompt})

    # This is for ConversationalRetrievalChain
    #test = qa({"question": query, "chat_history": chat_history})

    # This is for RetrievalQA Note: this is dictionnary with query and not with question like ConversationalRetrievalChain
    test = qa({"query": query})



    print(test)

    return test
    