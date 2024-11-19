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
        print("HERE0")
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=bucket_name, Key=key)

        # Step 2: Read the file content into a BytesIO stream
        print("HERE1")
        file_stream = io.BytesIO(response['Body'].read())

        # Step 3: Load the SQLite database into memory
        print("HERE2")
        conn = sqlite3.connect(':memory:')  # Create an in-memory SQLite database
        with conn:
            # Load the database content from the binary stream
            conn.executescript(file_stream.getvalue().decode('utf-8'))

        print("HERE3")
        # Step 4: Query the in-memory SQLite database
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print("Tables in the database:")
        for table in cursor.fetchall():
            print(table[0])

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
bucket_name = "your-s3-bucket-name"
key = "path/to/your/database.db"  # Replace with the path to your SQLite file in S3

read_sqlite_from_s3(bucket_name, key)

# Example usage
bucket_name = "felsen-bucket"
key = "dnd.db"  # Replace with the path to your SQLite file in S3

read_sqlite_from_s3(bucket_name, key)
