import boto3
import sqlite3
import io


def read_sqlite_from_s3(bucket_name, key):
    """
    Read and query an SQLite database directly from S3 without saving it to disk.

    :param bucket_name: Name of the S3 bucket.
    :param key: Path to the SQLite database file in the S3 bucket.
    """
    try:
        # Step 1: Connect to S3 and fetch the database file as a binary stream
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=bucket_name, Key=key)

        # Step 2: Read the file content into a BytesIO stream
        file_stream = io.BytesIO(response['Body'].read())

        # Step 3: Connect to the SQLite database in memory
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()

        # Step 4: Load the database from the file stream
        with io.BytesIO(file_stream.read()) as temp_file:
            conn.backup(sqlite3.connect(temp_file))

        # Example query: List all tables in the database
        print("Tables in the database:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for table in cursor.fetchall():
            print(table[0])

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


# Example usage
bucket_name = "felsen-bucket"
key = "dnd.db"  # Replace with the path to your SQLite file in S3

read_sqlite_from_s3(bucket_name, key)
