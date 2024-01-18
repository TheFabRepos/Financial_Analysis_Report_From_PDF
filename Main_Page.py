import streamlit as st
from google.cloud.sql.connector import Connector, IPTypes
import pg8000
import sqlalchemy
import os

st.set_page_config(
    page_title="Main Page",
    page_icon="📄",
)

@st.cache_resource
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

def get_list_collectiom() -> list[str]:
    
    engine:sqlalchemy.engine.base.Engine = connect_with_connector()
    with engine.connect() as db_conn:
        results = db_conn.execute(sqlalchemy.text("SELECT name from langchain_pg_collection")).fetchall()
        list_pgvector_collection = [res.name for res in results]
        return list_pgvector_collection




st.header("Chat with your financial statement")
st.subheader("Please select one collection:")


options = get_list_collectiom()
choice = st.radio("", options)

st.text_input("Your choice:", value=choice, disabled=True)
