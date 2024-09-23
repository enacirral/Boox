from bs4 import BeautifulSoup
import re
import logging

logger = logging.getLogger(__name__)
def parse_chapter_content(html):
    """解析章节内容"""
    soup = BeautifulSoup(html, 'html.parser')
    title_tag = soup.find('h1')
    title = title_tag.text if title_tag else ""
    content_tag = soup.find('div', class_='nesdetails')
    content = content_tag.text if content_tag else ""
    
    # 移除 "请分页阅读：" 及后面的页码链接
    content = re.sub(r'请分页阅读：.*$', '', content, flags=re.DOTALL)
    
    # 移除 "推荐阅读：" 及其后的内容
    content = re.sub(r'推荐阅读：.*$', '', content, flags=re.DOTALL)
    
    # 移除 "本章完" 及其后的内容
    content = re.sub(r'本章完.*$', '', content, flags=re.DOTALL)
    
    # 移除 "请关闭浏览器阅读模式" 的提示
    content = re.sub(r'请关闭浏览器阅读模式.*?等现象。', '', content, flags=re.DOTALL)
    
    # 移除 "If you are not a Chinese reader" 的提示
    content = re.sub(r'If you are not a Chinese reader.*?for translation\.', '', content, flags=re.DOTALL)
    
    # 移除 "If you can't read Chinese" 的提示
    content = re.sub(r'If you can\'t read Chinese.*?language you want\.', '', content, flags=re.DOTALL)
    
    # 移除多余的空行
    content = re.sub(r'\n\s*\n', '\n\n', content)
    
    return title, content.strip()

def get_all_page_links(html, base_url):
    """获取所有页面链接"""
    soup = BeautifulSoup(html, 'html.parser')
    page_links_div = soup.find('div', id='page-links')
    if not page_links_div:
        logger.warning("未找到分页链接")
        return []
    
    links = page_links_div.find_all('a')
    full_links = []
    for link in links:
        href = link.get('href')
        if href:
            if href.startswith('http'):
                full_links.append(href)
            else:
                full_links.append(base_url + href)
    
    logger.info(f"在页面中找到的链接：{full_links}")
    
    return full_links

def combine_content(chapters):
    """合并所有章节内容"""
    combined = []
    for i, (title, content) in enumerate(chapters):
        # 移除标题中的 "第X章" 部分
        clean_title = re.sub(r'^第\d+章\s*', '', title).strip()
        
        # 如果清理后的标题为空，使用原标题
        if not clean_title:
            clean_title = title
        
        # 添加章节标题和内容
        combined.append(f"第{i+1}章 {clean_title}\n{content}")
    
    return "\n\n".join(combined)