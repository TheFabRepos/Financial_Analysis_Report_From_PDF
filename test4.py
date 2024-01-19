import os
from typing import Any, List, Dict

from langchain_google_vertexai import VertexAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from retrieve_pgvector.rag_pgvector import PG_Vector_RAG
from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import PromptTemplate

COLLECTION_NAME = "Google_2022"

pgvector_retrieval = PG_Vector_RAG(
                        collection_name="Google_2022", 
                        embedding_function = VertexAIEmbeddings(model_name="textembedding-gecko@latest", 
                        project=os.getenv("PROJECT_ID"))
                        )


def run_llm(query: str, chat_history: List[Dict[str, Any]] = []) -> Any:



# You are a expert in extracting information from JSON content.
# Based on the JSON document below, what is the revenue in USA in 2021. Don\'t make up data, if the information cannot be found in the provided context with 100% certainty then just say not available in context. 
# Analysed if calculation is required, and if it is then detail step by step the approach and value used for the calculation.




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



    #system_message = "Using the provided context respond the given answer \n\n----context \n{context}"

    #custom_prompt = ChatPromptTemplate.from_messages( [ SystemMessagePromptTemplate.from_template(system_message), HumanMessagePromptTemplate.from_template("{question}"), ]


    test = qa({"question": query, "chat_history": []})
    
    return test["answer"]


if __name__ == "__main__":
    print(run_llm(query="Calculate the percentage growth in Google revenue between 2021 and 2022?"))