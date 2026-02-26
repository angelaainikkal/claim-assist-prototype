import boto3

s3 = boto3.client(
    "s3",
    aws_access_key_id="YOUR_KEY",
    aws_secret_access_key="YOUR_SECRET",
    region_name="ap-south-1"
)

def upload_file(file_path, filename):
    s3.upload_file(file_path, "your-bucket-name", filename)
    return f"https://your-bucket-name.s3.amazonaws.com/{filename}"