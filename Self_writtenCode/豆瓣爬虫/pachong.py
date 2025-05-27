import requests
from lxml import etree
import pandas as pd
import os
import time

"""
大创项目数据准备

本程序实现豆瓣书籍数据爬虫功能，支持根据不同标签
（如科幻、言情、武侠等）爬取对应类别的书籍信息。

使用说明：
1. 设置对应标签的URL（从豆瓣网站复制标签页面URL）。
2. 程序一次爬取一个标签下的多页数据。
3. 爬取数据包括书名、评分和基本信息（作者、出版社等）。
4. 数据最终保存到桌面Excel文件。

注意：
2025.4.10 注：目前豆瓣反爬策略加强，可能导致爬取失败。
"""

def get_headers():
    """
    构建请求头，模拟浏览器访问，避免被反爬机制阻挡。
    
    Returns:
        dict: 包含User-Agent的请求头信息。
    """
    db_header = {
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/128.0.0.0 Safari/537.36"
        )
    }
    return db_header


def get_html(basic_url):
    """
    发送HTTP GET请求，获取网页HTML内容。
    
    Args:
        basic_url (str): 目标网页URL。
        
    Returns:
        str: 返回网页的HTML文本，失败时返回空字符串。
    """
    try:
        db_book = requests.get(url=basic_url, headers=get_headers(), timeout=10)
        db_book_html = db_book.text
        return db_book_html
    except Exception as e:
        print("请求失败：", basic_url)
        print("错误信息：", e)
        return ""


def clean_basic_info(basic_info):
    """
    清洗并处理基础信息，去除换行符和多余空白，
    并将信息以 '/' 作为分隔符拆分成列表。
    
    Args:
        basic_info (list[str]): 包含原始基础信息的字符串列表。
        
    Returns:
        list[list[str]]: 清洗拆分后的基础信息二维列表。
    """
    basic_info = [info.replace("\n", "").strip().split("/") for info in basic_info]
    return basic_info


def clean_title(book_title):
    """
    清洗书名列表，去除换行符、空白字符及空字符串元素。
    
    Args:
        book_title (list[str]): 原始书名列表。
        
    Returns:
        list[str]: 清洗后的有效书名列表。
    """
    book_title = [info.replace("\n", "").strip() for info in book_title]
    book_title = [i for i in book_title if i != ""]
    return book_title


def parse_html(db_html, info=None):
    """
    解析网页HTML内容，提取书名、评分和基础信息。
    
    Args:
        db_html (str): 目标网页的HTML文本。
        info: 预留参数，当前未使用。
        
    Returns:
        list[tuple]: 返回包含(书名, 评分, 基础信息)的元组列表。
        
    XPath说明：
    - 书名、作者等基础信息位置：
      //*[@id="subject_list"]/ul/li[@class="subject-item"]/div[2]/div[1]/text()
    - 评分位置：
      //*[@id="subject_list"]/ul/li[@class="subject-item"]/div[2]/div[2]/span[2]/text()
    - 书名位置：
      //*[@id="subject_list"]/ul/li[@class="subject-item"]/div[2]/h2/a/text()
    """
    db_html = etree.HTML(db_html)

    basic_info = db_html.xpath(
        '//*[@id="subject_list"]/ul/li[@class="subject-item"]/div[2]/div[1]/text()'
    )
    basic_info = clean_basic_info(basic_info)

    rating_nums = db_html.xpath(
        '//*[@id="subject_list"]/ul/li[@class="subject-item"]/div[2]/div[2]/span[2]/text()'
    )

    book_title = db_html.xpath(
        '//*[@id="subject_list"]/ul/li[@class="subject-item"]/div[2]/h2/a/text()'
    )
    book_title = clean_title(book_title)

    all_data = list(zip(book_title, rating_nums, basic_info))

    return all_data


def build_url(base_url, page):
    """
    构建分页URL。
    
    Args:
        base_url (str): URL模板，含有格式化占位符 `{}`。
        page (int): 当前页的起始索引参数。
        
    Returns:
        str: 格式化后的完整URL。
    """
    return base_url.format(page)


def crawl_all_pages(base_url, start=0, end=8000, step=20):
    """
    遍历多个分页URL，循环爬取数据并合并。
    
    Args:
        base_url (str): URL模板。
        start (int): 起始页索引。
        end (int): 结束页索引（不包含）。
        step (int): 分页步长，豆瓣默认每页20条。
        
    Returns:
        list[tuple]: 所有页面爬取到的数据合并列表。
    """
    adata = []
    for page in range(start, end, step):
        basic_url = build_url(base_url, page)
        print(f"正在爬取第 {page // step + 1} 页，URL：{basic_url}")
        db_html = get_html(basic_url)
        all_data = parse_html(db_html)
        adata += all_data
        time.sleep(0.5)  # 避免请求过快触发反爬机制
    return adata


def get_desktop_path():
    """
    获取当前用户桌面目录路径。
    
    Returns:
        str: 用户桌面路径字符串。
    """
    return os.path.join(os.path.expanduser("~"), "Desktop")


def save_data_to_excel(data, filename="豆瓣书籍.xlsx"):
    """
    将爬取数据保存为Excel文件，默认保存在桌面。
    
    Args:
        data (list[tuple]): 需要保存的数据，包含书名、评分、基础信息。
        filename (str): 保存文件名，默认“豆瓣书籍.xlsx”。
    """
    df = pd.DataFrame(data, columns=["书名", "评分", "基本信息"])
    desktop_path = get_desktop_path()
    full_path = os.path.join(desktop_path, filename)
    df.to_excel(full_path, index=False)
    print(f"\n文件已保存至桌面：{full_path}")


def main():
    """
    主程序入口，设置目标标签URL，启动爬取流程，保存数据。
    """
    print("开始爬取豆瓣书籍数据...\n")
    base_url = "https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start={}&type=T"
    all_data = crawl_all_pages(base_url, 0, 8000, 20)
    save_data_to_excel(all_data)
    print("\n爬取完成！")


if __name__ == "__main__":
    main()
