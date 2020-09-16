import boto3
import dotenv
import os

dotenv.load_dotenv()

aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")

s3 = boto3.resource(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# for bucket in s3.buckets.all():
#     print(bucket.name)
BUCKET_NAME = "training-images-team-a"
OBJECT_NAME = 
FILE_NAME

s3.download_file(BUCKET_NAME, 'OBJECT_NAME', 'FILE_NAME')