from langchain_google_vertexai import VertexAIEmbeddings
from langchain.vectorstores.utils import DistanceStrategy
import os
from langchain_community.vectorstores.pgvector import PGVector
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from google.cloud.sql.connector import Connector, IPTypes
import pg8000
import sqlalchemy



PROJECT_ID = os.getenv("PROJECT_ID")
PGVECTOR_HOST=os.getenv("PGVECTOR_HOST")
PGVECTOR_PASSWORD = os.getenv("PGVECTOR_PASSWORD")
PGVECTOR_USER = os.getenv("PGVECTOR_USER")
PGVECTOR_DATABASE = os.getenv("PGVECTOR_DATABASE")
PGVECTOR_PORT = os.getenv("PGVECTOR_PORT")

#print (PROJECT_ID)

def embed():

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


    store.as_retriever()

    #store.add_documents(docs)
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





def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of Postgres.

    Uses the Cloud SQL Python Connector package.
    """
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.

    instance_connection_name = os.environ[
        "INSTANCE_CONNECTION_NAME"
    ]  # e.g. 'project:region:instance'

    db_user = os.environ["PGVECTOR_USER"]  # e.g. 'my-db-user'
    db_pass = os.environ["PGVECTOR_PASSWORD"]  # e.g. 'my-db-password'
    db_name = os.environ["PGVECTOR_DATABASE"]  # e.g. 'my-database'

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    # initialize Cloud SQL Python Connector object
    connector = Connector()

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=ip_type,
        )
        return conn

    # The Cloud SQL Python Connector can be used with SQLAlchemy
    # using the 'creator' argument to 'create_engine'
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        # ...
    )
    return pool





if __name__ == "__main__":

    engine:sqlalchemy.engine.base.Engine = connect_with_connector()
    
    with engine.connect() as db_conn:
        # insert into database
        # query database
        #result = db_conn.execute(sqlalchemy.text("SELECT name from langchain_pg_collection")).fetchall()
        result = db_conn.execute(sqlalchemy.text("SELECT name from langchain_pg_collection")).fetchall()





        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()

        # Do something with the results

        name_list = [r.name for r in result]

        print(name_list)

#        for r in result:
#            print(r.name)

    input("Press Enter to continue...")









