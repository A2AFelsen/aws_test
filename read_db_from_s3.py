import boto3
import sqlite3


s3 = boto3.resource('s3')
bucket_name = "felsen-bucket"
filename = "dnd.db"
obj = s3.Object(bucket_name, filename)
body = obj.get()['Body'].read()

conn = sqlite3.connect(body)
cursor = conn.cursor()
output = cursor.execute("SELECT * from npc_table").fetchall()
for entry in output:
    print(entry)

