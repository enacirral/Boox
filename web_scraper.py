import requests
from bs4 import BeautifulSoup
import time
import config
from content_parser import parse_chapter_content, get_all_page_links
import re

def fetch_webpage(url, retries=config.RETRY_TIMES):
    """获取网页内容"""
    headers = {'User-Agent': config.USER_AGENT}
    proxies = config.PROXY if config.USE_PROXY else None

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            config.logger.error(f"请求失败，尝试 {attempt + 1}/{retries}，错误: {e}")
            time.sleep(config.RETRY_WAIT)
    config.logger.error("请求失败，所有重试均已失败")
    return None

def get_chapter_links(url):
    """获取章节链接"""
    html = fetch_webpage(url)
    if html is None:
        return []
    soup = BeautifulSoup(html, 'html.parser')
    chapter_links = []
    for div in soup.find_all('div', class_='list category-list'):
        for a in div.find_all('a'):
            chapter_links.append(a['href'])
    return chapter_links

def get_full_chapter_content(chapter_url):
    """获取完整的章节内容（包括多页）"""
    base_url = '/'.join(chapter_url.split('/')[:-1]) + '/'
    html = fetch_webpage(chapter_url)
    if html is None:
        return "", ""
    
    title, content = parse_chapter_content(html)
    
    # 获取所有页面链接
    page_links = get_all_page_links(html, base_url)
    
    config.logger.info(f"获取到的页面链接：{page_links}")
    
    # 如果有多个页面，获取所有页面的内容
    if page_links:
        for link in page_links[1:]:  # 跳过第一个链接，因为我们已经处理过了
            config.logger.info(f"正在获取页面：{link}")
            page_html = fetch_webpage(link)
            if page_html is None:
                config.logger.warning(f"无法获取页面：{link}")
                continue
            _, page_content = parse_chapter_content(page_html)
            content += "\n" + page_content
    
    # 移除 "请分页阅读：" 及后面的页码链接
    content = re.sub(r'请分页阅读：.*$', '', content, flags=re.DOTALL)
    
    return title, content.strip()