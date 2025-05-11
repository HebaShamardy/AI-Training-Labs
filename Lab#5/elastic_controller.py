
import os
from elasticsearch import Elasticsearch

Elastic_APIKEY = os.getenv("Elastic_APIKEY")
Elastic_URL = os.getenv("Elastic_URL")



client = Elasticsearch(
  Elastic_URL,
  api_key=Elastic_APIKEY
)

# API key should have cluster monitor rights
client.info()

client.search(index="motor_collision", q="brooklyn")