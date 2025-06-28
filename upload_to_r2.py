# upload_to_r2.py
import boto3
import os
import yaml
from dotenv import load_dotenv
load_dotenv()

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_ENDPOINT = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"

session = boto3.session.Session()
s3 = session.client(
    service_name="s3",
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
    endpoint_url=R2_ENDPOINT,
    region_name=config["r2_region"],
)

def upload_to_r2(filename: str, path: str) -> str:
    try:
        key = f"assets/r2/{filename}"
        s3.upload_file(path, config["r2_bucket"], key, ExtraArgs={"ACL": "public-read"})
        print(f"☁️ R2 上傳成功: {key}")
        return config["cdn_r2_base"] + filename
    except Exception as e:
        print(f"⚠️ R2 上傳失敗: {e}")
        return None
