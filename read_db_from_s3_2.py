import boto3
import sqlite3
import io

def read_sqlite_from_s3(bucket_name, key):
    """
    Read and query an SQLite database stored in S3 directly into memory without saving it locally.

    :param bucket_name: Name of the S3 bucket.
    :param key: Path to the SQLite database file in the S3 bucket.
    """
    try:
        # Step 1: Connect to S3 and fetch the database file as a binary stream
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=bucket_name, Key=key)

        # Step 2: Read the file content into a BytesIO stream
        DND_DB = response['Body']
        conn = sqlite3.connect(DND_DB)
        cursor = conn.cursor()
        npc_list = cursor.execute("SELECT * from npc_table").fetchall()
        for npc in npc_list:
            print(npc)

    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
bucket_name = "felsen-bucket"
key = "dnd.db"  # Replace with the path to your SQLite file in S3

read_sqlite_from_s3(bucket_name, key)
