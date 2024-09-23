from web_scraper import  get_chapter_links, get_full_chapter_content
from content_parser import combine_content
from file_handler import save_to_file
from tqdm import tqdm
import config
import sys

def main():
    chapter_links = get_chapter_links(config.INDEX_URL)
    chapters = []
    
    # 创建进度条
    progress_bar = tqdm(total=len(chapter_links), desc="爬取进度", file=sys.stdout)
    
    for link in chapter_links:
        title, content = get_full_chapter_content(link)
        chapters.append((title, content))
        progress_bar.update(1)  # 更新进度条
    
    progress_bar.close()  # 关闭进度条
    
    all_content = combine_content(chapters)
    save_to_file(all_content, config.OUTPUT_FILE)
    config.logger.info(f"已保存所有章节内容到文件：{config.OUTPUT_FILE}")

if __name__ == "__main__":
    main()