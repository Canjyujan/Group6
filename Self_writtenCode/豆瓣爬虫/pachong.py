import requests
from lxml import etree
import pandas as pd
import os
import time

"""
大创项目数据准备
本程序实现爬虫爬取豆瓣书籍数据的功能
根据不同标签对应不同URL进行设置
一次只能爬取一个标签的书籍
如科幻、言情、武侠等
对应URL直接去豆瓣网网上复制就行
"""

"""
2025.4.10注：现在好像爬不了了=_=
"""


def get_headers():
    """构建请求头"""
    db_header = {
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/128.0.0.0 Safari/537.36"
        )
    }
    return db_header


def get_html(basic_url):
    """发送请求获取网页HTML数据"""
    try:
        db_book = requests.get(url=basic_url, headers=get_headers(), timeout=10)
        db_book_html = db_book.text
        return db_book_html
    except Exception as e:
        print("请求失败：", basic_url)
        print("错误信息：", e)
        return ""


def clean_basic_info(basic_info):
    """清洗基础信息，去除换行和空格，并拆分字符串"""
    basic_info = [info.replace("\n", "").strip().split("/") for info in basic_info]
    return basic_info


def clean_title(book_title):
    """清洗书名，去除多余符号和空字符串"""
    book_title = [info.replace("\n", "").strip() for info in book_title]
    book_title = [i for i in book_title if i != ""]
    return book_title


def parse_html(db_html, info=None):
    """
    解析HTML，提取书名、评分和基础信息
    XPath路径参考注释：
    //*[@id="subject_list"]/ul/li[@class="subject-item"]/div[2]/div[1]
    //*[@id="content"]/div/div[1]/ul/li[@class="media clearfix"]/div[2]/p[1]/text()
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
    """拼接URL"""
    return base_url.format(page)


def crawl_all_pages(base_url, start=0, end=8000, step=20):
    """爬取多个页面数据"""
    adata = []
    for page in range(start, end, step):
        basic_url = build_url(base_url, page)
        print(page)  # 打印页数方便观察爬取进度
        db_html = get_html(basic_url)
        all_data = parse_html(db_html)
        adata += all_data
        time.sleep(0.5)  # 线程休眠，绕过反爬机制
    return adata


def get_desktop_path():
    """获取桌面路径"""
    return os.path.join(os.path.expanduser("~"), "Desktop")


def save_data_to_excel(data, filename="豆瓣书籍.xlsx"):
    """保存数据到Excel文件，默认保存到桌面"""
    df = pd.DataFrame(data, columns=["书名", "评分", "基本信息"])
    desktop_path = get_desktop_path()
    full_path = os.path.join(desktop_path, filename)
    df.to_excel(full_path, index=False)
    print(f"\n文件保存至桌面：{full_path}")


def main():
    print("正在爬取...\n")
    base_url = "https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start={}&type=T"
    all_data = crawl_all_pages(base_url, 0, 8000, 20)
    save_data_to_excel(all_data)
    print("\n爬取完成")


if __name__ == "__main__":
    main()
