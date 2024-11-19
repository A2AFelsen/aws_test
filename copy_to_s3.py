import boto3


def upload_to_s3(file_path, bucket_name, s3_key):
    """
    Upload a file to an S3 bucket.

    :param file_path: Path to the file on the EC2 instance.
    :param bucket_name: Name of the S3 bucket.
    :param s3_key: Key (path) under which to store the file in S3.
    """
    try:
        # Create an S3 client
        s3_client = boto3.client('s3')

        # Upload the file
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"File '{file_path}' successfully uploaded to '{bucket_name}/{s3_key}'")
    except Exception as e:
        print(f"Error uploading file: {e}")


# Example usage
file_path = "/var/www/html/dnd.db"  # Local file path on EC2
bucket_name = "felsen-bucket"  # S3 bucket name
s3_key = "dnd.db"  # Key in the S3 bucket

upload_to_s3(file_path, bucket_name, s3_key)
