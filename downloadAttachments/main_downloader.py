import json
import requests
import os
from urllib.parse import urljoin

# FastDFS 的 HTTP 服务基础URL
BASE_URL = 'http://20.201.37.174:8888/group1/'

# 本地保存目录
LOCAL_SAVE_DIR = './downloads'

# 创建保存目录，如果不存在
os.makedirs(LOCAL_SAVE_DIR, exist_ok=True)

# 从 JSON 文件读取关联关系
with open('attachments.json', 'r', encoding='utf-8') as jsonfile:
    attachments = json.load(jsonfile)

    for attachment in attachments:
        id = attachment['ID']
        filename = attachment['FileName']

        # 构造文件的完整 URL
        file_url = urljoin(BASE_URL, id)

        try:
            # 下载文件
            response = requests.get(file_url, stream=True)
            response.raise_for_status()

            # 保存文件并重命名
            local_path = os.path.join(LOCAL_SAVE_DIR, filename)
            with open(local_path, 'wb') as out_file:
                for chunk in response.iter_content(chunk_size=8192):
                    out_file.write(chunk)

            print(f"文件 {id} 已下载并重命名为 {filename}")
        except requests.exceptions.RequestException as e:
            print(f"下载 {file_url} 时出错: {e}")

print("下载完成。")