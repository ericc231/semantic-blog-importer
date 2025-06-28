import base64

with open("cover_b64.txt", "r") as f:
    b64_data = f.read()

with open("cover.png", "wb") as img_file:
    img_file.write(base64.b64decode(b64_data))

print("✅ 圖片已成功儲存為 cover.png")
