import os
import logging

# 代理设置
USE_PROXY = True
PROXY = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

# 用户代理设置
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# 基础URL
BASE_URL = "https://www.tangsanbooks.com"

# 小说索引页URL
INDEX_URL = f"{BASE_URL}/xs/zhiguaishu"

# 输出目录
OUTPUT_DIR = "Boox"

# 输出文件名
OUTPUT_FILENAME = "志怪书.txt"

# 完整的输出文件路径
OUTPUT_FILE = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)

# 重试次数
RETRY_TIMES = 3

# 重试等待时间（秒）
RETRY_WAIT = 2

# 日志配置
LOG_LEVEL = logging.WARNING
LOG_FILE = 'scraper.log'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
LOG_MAX_SIZE = 5 * 1024 * 1024  # 5 MB
LOG_BACKUP_COUNT = 2

# 配置日志
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, filename=LOG_FILE)
logger = logging.getLogger(__name__)