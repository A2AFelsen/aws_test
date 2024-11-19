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
        file_stream = io.BytesIO(response['Body'].read())

        # Step 3: Create an in-memory SQLite database
        mem_conn = sqlite3.connect(':memory:')  # Create an in-memory SQLite database

        # Step 4: Use backup to load the data into the in-memory database
        with mem_conn:
            # Create a temporary file in-memory using SQLite backup
            with sqlite3.connect(':memory:') as temp_conn:
                file_stream.seek(0)  # Reset the stream to the start
                temp_conn.backup(mem_conn)

        # Step 5: Query the in-memory SQLite database
        cursor = mem_conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print("Tables in the database:")
        for table in cursor.fetchall():
            print(table[0])

        # Clean up connections
        mem_conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
bucket_name = "felsen-bucket"
key = "dnd.db"  # Replace with the path to your SQLite file in S3

read_sqlite_from_s3(bucket_name, key)
