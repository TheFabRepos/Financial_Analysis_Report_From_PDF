from langchain_google_vertexai import VertexAIEmbeddings
from langchain.vectorstores.utils import DistanceStrategy
import os
from langchain_community.vectorstores.pgvector import PGVector
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

PROJECT_ID = os.getenv("PROJECT_ID")
PGVECTOR_HOST=os.getenv("PGVECTOR_HOST")
PGVECTOR_PASSWORD = os.getenv("PGVECTOR_PASSWORD")
PGVECTOR_USER = os.getenv("PGVECTOR_USER")
PGVECTOR_DATABASE = os.getenv("PGVECTOR_DATABASE")
PGVECTOR_PORT = os.getenv("PGVECTOR_PORT")

#print (PROJECT_ID)


embeddings = VertexAIEmbeddings(
   model_name="textembedding-gecko@latest", project=PROJECT_ID
)

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
    host=os.environ.get("PGVECTOR_HOST", "localhost"),
    port=int(os.environ.get("PGVECTOR_PORT", "5432")),
    database=os.environ.get("PGVECTOR_DATABASE", "postgres"),
    user=os.environ.get("PGVECTOR_USER", "postgres"),
    password=os.environ.get("PGVECTOR_PASSWORD", "postgres"),
)

#docs:list[str] = ["The quick brown fox jumps over the lazy dog", "This is my test"]

path = "JSONL_Previous_Test/json/"
dir_list = os.listdir(path)
 
print("Files and directories in '", path, "' :")
 
# prints all files
print(dir_list)
print (len(dir_list))


COLLECTION_NAME = "Google"


store = PGVector(
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
    embedding_function=embeddings,
    pre_delete_collection = True
)

try:
    for i, file in enumerate(dir_list):
        loader = TextLoader(f"JSONL_Previous_Test/json/{file}")
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        store.add_documents(docs)
except:
    print ('error')


input ('Press Enter to continue...')

