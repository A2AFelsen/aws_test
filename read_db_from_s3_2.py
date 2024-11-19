import boto3

def download_file_from_s3(bucket_name, s3_key, local_file_path):
    """
    Download a file from an S3 bucket to a local path on the EC2 instance.

    :param bucket_name: The name of the S3 bucket.
    :param s3_key: The key (path) to the file in the S3 bucket.
    :param local_file_path: The local file path where the file should be saved.
    """
    try:
        # Create an S3 client
        s3 = boto3.client('s3')

        # Download the file
        s3.download_file(bucket_name, s3_key, local_file_path)

        print(f"File downloaded successfully from s3://{bucket_name}/{s3_key} to {local_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
local_file_path = "/var/www/html/dnd.db"  # Local file path on EC2
bucket_name = "felsen-bucket"  # S3 bucket name
s3_key = "dnd.db"  # Key in the S3 bucket

download_file_from_s3(bucket_name, s3_key, local_file_path)

