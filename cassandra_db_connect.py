
import cassandra
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json

# This secure connect bundle is autogenerated when you download your SCB, 
# if yours is different update the file name below
cloud_config= {
  'secure_connect_bundle': 'secure-connect-koob404-db.zip'
}

# This token JSON file is autogenerated when you download your token, 
# if yours is different update the file name below
with open("koob404_db-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]
ASTRA_DB_KEYSPACE = secrets["keyspace"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

DEBUG=False # switch to True if debug is needed

if DEBUG:
  print (f"Cassandra db version: {cassandra.__version__}")
  row = session.execute("select release_version from system.local").one()
  if row:
    print(f"Connected to db row 0 = {row[0]}")
  else:
    print("An error occurred when connecting cassandra db.")