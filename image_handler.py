# image_handler.py
import os
import hashlib
import base64
import yaml
from upload_to_pages import upload_to_pages
from upload_to_r2 import upload_to_r2

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

def save_base64_image(base64_str: str, slug: str) -> str:
    header, b64data = base64_str.split(',', 1)
    mime = header.split(';')[0].split(':')[-1]
    ext = mime.split('/')[-1]
    binary_data = base64.b64decode(b64data)
    hash_id = hashlib.sha256(binary_data).hexdigest()[:10]
    filename = f"{slug}-{hash_id}.{ext}"

    target = "pages" if len(binary_data) < config["image_size_threshold"] else "r2"
    out_dir = os.path.join(config["local_assets_dir"], target)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, filename)

    with open(path, 'wb') as f:
        f.write(binary_data)

    if target == "pages":
        upload_to_pages(filename, path)
        return config["cdn_pages_base"] + filename
    else:
        return upload_to_r2(filename, path) or (config["cdn_r2_base"] + filename)
