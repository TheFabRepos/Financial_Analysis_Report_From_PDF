import base64
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, Image
from langchain_google_vertexai import VertexAIEmbeddings
from google.cloud import bigquery
from langchain.vectorstores.utils import DistanceStrategy
from langchain_community.vectorstores import BigQueryVectorSearch


# val = """{
#   "table_header": [
#     "Net income",
#     "Other comprehensive income (loss)",
#     "Change in foreign currency translation adjustment",
#     "Change in net unrealized gains (losses)",
#     "Less: reclassification adjustment for net (gains) losses included in net income",
#     "Net change in net unrealized gains (losses)",
#     "Cash flow hedges:",
#     "Less: reclassification adjustment for net (gains) losses included in net income",
#     "Net change, net of income tax benefit (expense) of $11, $22), and $110",
#     "Comprehensive income"
#   ],
#   "table_data": [
#     [
#       40269,
#       1139,
#       1339,
#       1313,
#       -513,
#       800,
#       42,
#       -116,
#       562,
#       42134
#     ],
#     [
#       76033,
#       1442,
#       -1836,
#       -1312,
#       -64,
#       -1376,
#       716,
#       -154,
#       566,
#       73777
#     ],
#     [
#       59972,
#       822,
#       -
#       -4720,
#       1007,
#       -
#       -2313,
#       1275,
#       -
#       -431,
#       53992
#     ]
#   ],
#   "table_date": {
#     "month": 12,
#     "year": 2021
#   }
# }"""

# #print (val.index('{'))



# substr = "{"
# inserttxt = '\n "description": "valeur", \n  "source": '

# idx = val.index(substr)
# val = val[:(idx+1)] + inserttxt + val[(idx+1):]

# print(val)
# 'thisissometextXXthatiwrote'

PROJECT_ID = "testfab-362608"
REGION = "US"
DATASET = "my_langchain_dataset"
TABLE = "doc_and_vectors"


embedding = VertexAIEmbeddings(
    model_name="textembedding-gecko@latest", project=PROJECT_ID
)

client = bigquery.Client(project=PROJECT_ID, location=REGION)
client.create_dataset(dataset=DATASET, exists_ok=True)


store = BigQueryVectorSearch(
    project_id=PROJECT_ID,
    dataset_name=DATASET,
    table_name=TABLE,
    location=REGION,
    embedding=embedding,
    distance_strategy=DistanceStrategy.EUCLIDEAN_DISTANCE,
)


all_texts = ["Apples and oranges", "Cars and airplanes", "Pineapple", "Train", "Banana"]
metadatas = [{"len": len(t)} for t in all_texts]

store.add_texts(all_texts, metadatas=metadatas)

query = "I'd like a fruit."
docs = store.similarity_search(query)
print(docs)


