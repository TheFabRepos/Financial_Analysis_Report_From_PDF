from langchain_google_vertexai import VertexAIEmbeddings
import os
from langchain_community.vectorstores.pgvector import PGVector
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from google.cloud.sql.connector import Connector, IPTypes
import google.api_core.exceptions as google_exceptions
from ratelimit import limits, sleep_and_retry
from backoff import on_exception, expo

def embed_file_in_path(file_path:str, collection_name:str):

    embeddings = VertexAIEmbeddings(model_name="textembedding-gecko@latest", project=os.getenv("PROJECT_ID"))

    connection_string = PGVector.connection_string_from_db_params (

        driver=os.getenv("PGVECTOR_DRIVER", "psycopg2"),
        host=os.getenv("PGVECTOR_HOST"),
        port=int(os.getenv("PGVECTOR_PORT")),
        database=os.getenv("PGVECTOR_DATABASE"),
        user=os.getenv("PGVECTOR_USER"),
        password=os.getenv("PGVECTOR_PASSWORD"),
    )

    dir_list = os.listdir(file_path)
 
    store = PGVector(
        collection_name=collection_name,
        connection_string=connection_string,
        embedding_function=embeddings,
        pre_delete_collection = True
    )

    #store.as_retriever()

    #try:
    for i, file in enumerate(dir_list):
        loader = TextLoader(f"{file_path}/{file}")
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        embed_docs(docs=docs, store=store )
        #store.add_documents(docs)
    #except:
    #    print ('error')
    #input ('Press Enter to continue...')


@sleep_and_retry # If there are more request to this function than rate, sleep shortly
@on_exception(expo, google_exceptions.ResourceExhausted, max_tries=10) # if we receive exceptions from Google API, retry
@limits(calls=60, period=60)
def embed_docs(docs: list[Document], store: PGVector):
    store.add_documents(docs)
