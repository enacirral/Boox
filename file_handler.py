import os
import config

def save_to_file(content, filename):
    """保存内容到文件"""
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)